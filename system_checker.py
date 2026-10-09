import platform
import subprocess
import shutil
import json
import socket


print("Operating System:", platform.system())
print("Computer:", platform.node())
print("Architecture:", platform.machine())

def get_cpu_info():
    system = platform.system()

    if system == "Darwin":
        # macOS
        try:
            result = subprocess.run(
                ["sysctl", "-n", "machdep.cpu.brand_string"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
        except (OSError, subprocess.TimeoutExpired):
            pass

    elif system == "Linux":
        # Linux: сначала ищем модель в /proc/cpuinfo
        try:
            with open("/proc/cpuinfo", "r", encoding="utf-8") as file:
                for line in file:
                    if ":" not in line:
                        continue

                    key, value = line.split(":", 1)
                    key = key.strip().lower()
                    value = value.strip()

                    if key == "model name" and value and value != "-":
                        return value
        except OSError:
            pass

        # Если модели нет, пробуем получить производителя через lscpu
        try:
            result = subprocess.run(
                ["lscpu"],
                capture_output=True,
                text=True,
                timeout=5
            )

            vendor = ""
            model = ""

            for line in result.stdout.splitlines():
                if ":" not in line:
                    continue

                key, value = line.split(":", 1)
                key = key.strip().lower()
                value = value.strip()

                if key == "vendor id":
                    vendor = value
                elif key == "model name" and value not in ("", "-", "0"):
                    model = value

            if model:
                return model

            architecture = platform.machine().lower()

            if vendor and architecture in ("aarch64", "arm64"):
                return f"{vendor} ARM64"

            if vendor:
                return f"{vendor} CPU"

        except (OSError, subprocess.TimeoutExpired):
            pass

    elif system == "Windows":
        # Windows: получаем название через системную информацию
        try:
            result = subprocess.run(
                [
                    "powershell.exe",
                    "-NoProfile",
                    "-Command",
                    "(Get-CimInstance Win32_Processor | "
                    "Select-Object -First 1 -ExpandProperty Name)"
                ],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
        except (OSError, subprocess.TimeoutExpired):
            pass

    # Запасной вариант, если точное название не удалось получить
    architecture = platform.machine().lower()

    if architecture in ("aarch64", "arm64"):
        return "ARM64 CPU"

    if architecture in ("x86_64", "amd64"):
        return "x86-64 CPU"

    return f"{architecture} CPU" if architecture else "Unknown CPU"


cpu = get_cpu_info()
logical_cpus = __import__("os").cpu_count() or 1

print("CPU:", cpu)
print("Logical CPUs:", logical_cpus)


def get_total_memory_bytes():
    system = platform.system()

    if system == "Darwin":
        # macOS
        result = subprocess.run(
            ["sysctl", "-n", "hw.memsize"],
            capture_output=True,
            text=True,
            check=True
        )
        return int(result.stdout.strip())

    elif system == "Linux":
        # Linux
        with open("/proc/meminfo", "r", encoding="utf-8") as file:
            for line in file:
                if line.startswith("MemTotal:"):
                    memory_kb = int(line.split()[1])
                    return memory_kb * 1024

        raise RuntimeError("Could not determine total RAM on Linux")

    elif system == "Windows":
        # Windows
        import ctypes
        from ctypes import wintypes

        class MEMORYSTATUSEX(ctypes.Structure):
            _fields_ = [
                ("dwLength", wintypes.DWORD),
                ("dwMemoryLoad", wintypes.DWORD),
                ("ullTotalPhys", ctypes.c_ulonglong),
                ("ullAvailPhys", ctypes.c_ulonglong),
                ("ullTotalPageFile", ctypes.c_ulonglong),
                ("ullAvailPageFile", ctypes.c_ulonglong),
                ("ullTotalVirtual", ctypes.c_ulonglong),
                ("ullAvailVirtual", ctypes.c_ulonglong),
                ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
            ]

        status = MEMORYSTATUSEX()
        status.dwLength = ctypes.sizeof(status)

        success = ctypes.windll.kernel32.GlobalMemoryStatusEx(
            ctypes.byref(status)
        )

        if not success:
            raise ctypes.WinError()

        return status.ullTotalPhys

    else:
        raise RuntimeError(
            f"Unsupported operating system: {system}"
        )


memory_bytes = get_total_memory_bytes()
memory_gb = memory_bytes / (1024 ** 3)
print("RAM:", round(memory_gb, 1), "GB")

disk = shutil.disk_usage("/")
total, used, free = disk
print("Total disk space (GB):", round(total / (1024 ** 3), 1), "GB")
print("Used disk space (GB):", round(used / (1024 ** 3), 1), "GB")
print("Free disk space (GB):", round(free / (1024 ** 3), 1), "GB")

def get_local_ip():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        sock.connect(("8.8.8.8", 80))
        return sock.getsockname()[0]

    except OSError:
        return ""

    finally:
        sock.close()


local_ip = get_local_ip()
print("Local IP:", local_ip)

def check_internet():
    system = platform.system()

    if system == "Windows":
        command = ["ping", "-n", "1", "8.8.8.8"]
    else:
        command = ["ping", "-c", "1", "8.8.8.8"]

    try:
        connection = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=5
        )

        print("Ping return code:", connection.returncode)

        return connection.returncode == 0, connection.returncode

    except subprocess.TimeoutExpired:
        print("Network check: TIMEOUT")
        return False, None

    except OSError as error:
        print("Network check error:", error)
        return False, None


internet_available, ping_return_code = check_internet()
print("Internet:", internet_available)

system_info = {}
system_info["operating_system"] = platform.system()
system_info["computer"] = platform.node()
system_info["architecture"] = platform.machine()
system_info["cpu"] = cpu
system_info["logical_cpus"] = logical_cpus
system_info["ram_gb"] = round(memory_gb, 1)
system_info["disk_total_gb"] = round(total / (1024 ** 3), 1)
system_info["disk_used_gb"] = round(used / (1024 ** 3), 1)
system_info["disk_free_gb"] = round(free / (1024 ** 3), 1)
system_info["local_ip"] = local_ip
system_info["ping_return_code"] = ping_return_code
system_info["internet_available"] = internet_available
with open("system_info.json", "w", encoding="utf-8") as file:
    json.dump(system_info, file, indent=4)
    print("JSON file created: system_info.json")
print("\n=== SYSTEM INFORMATION ===")
print("Network check:", "OK" if internet_available else "FAILED")
