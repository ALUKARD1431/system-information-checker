import platform
import subprocess
import shutil
import json


print("Operating System:", platform.system())
print("Computer:", platform.node())
print("Architecture:", platform.machine())

cpu = subprocess.run(["sysctl", "-n", "machdep.cpu.brand_string"], capture_output=True, text=True).stdout.strip()
print("CPU:", cpu)

memory_bytes = int(subprocess.run(["sysctl", "-n", "hw.memsize"], capture_output=True, text=True).stdout.strip())
memory_gb = memory_bytes / (1024 ** 3)
print("RAM:", memory_gb, "GB")

disk = shutil.disk_usage("/")
total, used, free = disk
print("Total disk space (GB):", round(total / (1024 ** 3), 1), "GB")
print("Used disk space (GB):", round(used / (1024 ** 3), 1), "GB")
print("Free disk space (GB):", round(free / (1024 ** 3), 1), "GB")

local_ip = subprocess.run(["ipconfig", "getifaddr", "en0"], capture_output=True, text=True).stdout.strip()
print("Local IP:", local_ip)

ping_return_code = None
try:
    connection = subprocess.run(["ping", "-c", "1", "8.8.8.8"], capture_output=True, text=True, timeout=5)
    print("Ping return code:", connection.returncode)
    internet_available = connection.returncode == 0
except subprocess.TimeoutExpired:
    print("Network check: TIMEOUT")
    internet_available = False
print("Internet:", internet_available)

system_info = {}
system_info["operating_system"] = platform.system()
system_info["computer"] = platform.node()
system_info["architecture"] = platform.machine()
system_info["cpu"] = cpu
system_info["ram_gb"] = round(memory_gb, 1)
system_info["disk_total_gb"] = round(total / (1024 ** 3), 1)
system_info["disk_used_gb"] = round(used / (1024 ** 3), 1)
system_info["disk_free_gb"] = round(free / (1024 ** 3), 1)
system_info["local_ip"] = local_ip
system_info["ping_return_code"] = connection.returncode \
    if internet_available \
    else None
system_info["internet_available"] = internet_available
with open("system_info.json", "w", encoding="utf-8") as file:
    json.dump(system_info, file, indent=4)
    print("JSON file created: system_info.json")
print("\n=== SYSTEM INFORMATION ===")
print("Network check:", "OK" if internet_available else "FAILED")
