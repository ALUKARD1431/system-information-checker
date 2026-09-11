# System Information Checker

Ein kleines Python-Tool zur automatisierten Erfassung grundlegender System- und Netzwerkinformationen.

## Funktionen

* Erkennung des Betriebssystems und Computernamens
* Erkennung von CPU und Arbeitsspeicher (RAM)
* Anzeige des gesamten, belegten und freien Speicherplatzes
* Ermittlung der lokalen IPv4-Adresse
* Einfache Prüfung der Netzwerkverbindung mit ping
* Speicherung der gesammelten Informationen als JSON-Datei

## Verwendete Technologien

* Python
* Python Standard Library
* platform
* subprocess
* shutil
* socket
* json

## Ziel des Projekts

Dieses Projekt wurde als praktische Python-Übung entwickelt, um Kenntnisse in den Bereichen Systemadministration, Netzwerkdiagnose und Automatisierung anzuwenden und zu vertiefen.

Die Themen sind besonders relevant für eine Ausbildung zum Fachinformatiker für Systemintegration.

## Beispielausgabe

Das Programm erstellt eine system_info.json-Datei mit strukturierten Systeminformationen.

Die automatisch erzeugte JSON-Datei wird über .gitignore vom Git-Repository ausgeschlossen, da sie maschinenspezifische Informationen wie den Computernamen und die lokale IP-Adresse enthalten kann.

## Plattform

Das Projekt wurde unter macOS entwickelt und getestet.

Einige verwendete Systembefehle, wie sysctl und ipconfig, sind macOS-spezifisch.

## Mögliche Erweiterungen

* Unterstützung für Windows und Linux
* Detailliertere Netzwerkdiagnose
* Automatische Erkennung der verwendeten Netzwerkschnittstelle
* Weitere Systeminformationen
* Erweiterte Fehlerbehandlung