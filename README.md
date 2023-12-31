# Schwachstellenmgmt:
Fortgechrittenenpraktikum zum Thema: Entwicklung eines sicheren Kommunikationswegs zur Benachrichtigung von Verantwortlichen über Schwachstellen

### Vorbereitung zum Starten: 
    1. IP_Email.json nach dem darin dargestellten Aufbau ausfüllen 
    2. Passwörter und Links in der credentials.txt Datei einfügen
    3. Starten des Skriptes über vulnerabilityManagement.py 
        - Beim Starten des Skriptes wird der Link zum single_hosts - Ordner erfragt
        - Beim Starten des Skriptes wird die Möglichkeit gegeben die Gültigkeit des Links zu der Zip-Datei selbst zu wählen (Standardwert ist XXX)


### Inhalt eines Greenbone-Reports
- Ordner "single_hosts"
    - Pro Host gibt es eine PDF (Beispielname: uni_heidelberg_Medium_[IP Adresse].pdf)
- CSV Datei mit IP und Hostname aller im Report enthaltenen Auffälligkeiten
- Sonstige Dateien (HTML, README,...)

- wichtig ist der single_hosts Ordner mit den entsprechenden PDFs

### Zusätzlich benötigte Informationen
- JSON Datei mit Zuordnung von IP-Adressen zu E-Mail Adressen, der Verantwortlichen

### Aufgaben/Schritte:
    1. Login Nextcloud 
    2. Die einzelnen PDF-Dateien aus dem Report werden nach der E-Mail Adresse sortiert und in eine ZIP-Datei verpackt
        - JSON Datei mit Mapping IP auf E-Mail miteinbeziehen und die IP-Adressen mit den Namen der PDF-Dateien (uni_heidelberg_Medium_[IP Adresse].pdf) vergleichen 
        - Alle PDFs gruppiert nach den E-Mail Adressen werden in einen gemeinsamen Ordner ablegen
        - Daraus werden ZIP-Dateien erstellt ([IP-Adresse].zip)
        - Die ZIP Datei wird mit einem Passwort geschützt
    3. Die Zip-Dateien werden in die Nextcloud geuploadet
        - Der Share der Nextcloud wird ebenfalls mit einem Passwort geschützt
        - Es wird ein Link erzeugt, der direkt zu der geuploadeten Datei führt
        - Der Link ist nur x Tage gültig(Nach dem Starten des Skriptes wählbar)
    4. Es werden 2 One-Time-Links erstellt (https://onetimesecret.urz.uni-heidelberg.de:443)
        - Können nur einmal geöffnet werden 
        - Sichern die Kommunikation der Passwörter für die Nextcloud und für die ZIP-Datei ab
    5. Es werden zwei verschiedene E-Mails versendet an einen Empfänger
        1. Enthält den Link zur Datei auf der Nextcloud + One-Time-Link der das Passwort für die ZIP-Datei enthält
        2. Enthält einen One-Time-Link der das Passwort für die Nextcloud enthält
    6. Die Dateien auf der Nextcloud werden nach x Tagen gelöscht
        - Hierfür wurde ein Tag angelegt mit dem Namen "Greenbone Report"
        - Nach https://apps.nextcloud.com/apps/files_retention werden alle Dateien mit dem Tag "Greenbone Report" nach X Tagen gelöscht