# System Information Checker

Ein plattformübergreifendes Python-Tool zur Erfassung grundlegender System- und Netzwerkinformationen unter macOS, Linux und Windows.

## Funktionen

- Erkennung des Betriebssystems und Computernamens
- Erkennung der CPU-Architektur und des Prozessormodells, sofern verfügbar
- Ermittlung der Anzahl logischer Prozessoren
- Erfassung des gesamten Arbeitsspeichers (RAM)
- Anzeige des gesamten, belegten und freien Speicherplatzes
- Ermittlung der lokalen IP-Adresse
- Prüfung der Netzwerkverbindung mithilfe von `ping`
- Speicherung der gesammelten Informationen im JSON-Format

## Unterstützte Betriebssysteme

- macOS
- Linux
- Windows

Das Programm verwendet je nach Betriebssystem unterschiedliche Methoden, um Systeminformationen abzurufen. Welche Details verfügbar sind, hängt auch von der Hardware und der verwendeten Virtualisierungsumgebung ab.

## Verwendete Technologien

- Python 3
- Python-Standardbibliothek
- `platform`
- `subprocess`
- `shutil`
- `socket`
- `json`
- `ctypes` (für Windows-spezifische Systeminformationen)

Es werden keine zusätzlichen Python-Pakete benötigt.

## Verwendung

**macOS und Linux:**

```bash
python3 system_checker.py
```

**Windows:**

```powershell
py system_checker.py
```

Das Programm gibt die ermittelten Informationen im Terminal aus und erstellt die Datei `system_info.json` im aktuellen Arbeitsverzeichnis.

## JSON-Ausgabe

Die Datei `system_info.json` enthält strukturierte Informationen über das System, darunter Betriebssystem, Computername, CPU, Prozessoranzahl, RAM, Festplattenbelegung, lokale IP-Adresse und das Ergebnis der Netzwerkprüfung.

Die automatisch erzeugte JSON-Datei wird nicht in das Git-Repository aufgenommen, da sie systemspezifische Informationen wie den Computernamen und die lokale IP-Adresse enthalten kann.

## Einschränkungen

- Das genaue Prozessormodell ist nicht auf jedem System verfügbar, insbesondere in virtuellen Maschinen.
- Ein fehlgeschlagener Ping bedeutet nicht zwingend, dass keine Internetverbindung besteht. ICMP-Anfragen können beispielsweise durch Firewalls blockiert werden.
- Die lokale IP-Adresse kann unter bestimmten Netzwerkbedingungen nicht ermittelt werden.

## Projektziel

Dieses Projekt dient als praktische Python-Übung und vertieft Kenntnisse in den Bereichen Systemadministration, Netzwerkdiagnose und Automatisierung.

Die behandelten Themen sind besonders relevant für eine Ausbildung zum Fachinformatiker für Systemintegration.
