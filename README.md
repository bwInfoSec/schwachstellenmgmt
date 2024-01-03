# Schwachstellenmgmt:
Fortgechrittenenpraktikum zum Thema: Entwicklung eines sicheren Kommunikationswegs zur Benachrichtigung von Verantwortlichen über Schwachstellen

# Vorbereitung zum Starten: 
    1. IP_Email.csv Datei einfügen in das Hauptverzeichnis (in welchem auch die .py Dateien liegen)
        Aufbau: 
                    IP,Email
                    [IP],[Email]
                    [IP],[Email]
                    [IP],[Email]
                    ...

    2. Den aktuellen Report einfügen in den Ordner "current_report"
        Aufbau: 
                current_report
                    single_hosts
                        pdf
                        ...
                    uni_heidelberg_hosts.csv
                    ...

    3. Passwörter und Links einfügen
        - Nextcloud Zugangsdaten in vulnerabilityManagement.py
        - SMTP Informationen in email_functions.py
        - One-Time-Secret Zugangsdaten in secret_functions.py

    4. Starten des Skriptes über vulnerabilityManagement.py 


# Inhalt eines Greenbone-Reports
- Ordner "single_hosts"
    - Pro Host gibt es eine PDF (Beispielname: uni_heidelberg_Medium_[IP Adresse].pdf)
- CSV Datei mit IP und Hostname aller im Report enthaltenen Auffälligkeiten
- Sonstige Dateien (HTML, README,...)

- wichtig ist der single_hosts Ordner mit den entsprechenden PDFs

# Zusätzlich benötigte Informationen
- CSV Datei mit Zuordnung von IP-Adressen auf E-Mail Adressen, der Verantwortlichen

# Aufgaben/Schritte:
1. Login in der Nextcloud 
2. Sicherstellen, dass alle restlichen (ZIP)-Dateien, die noch in der Nextcloud vorhanden sind, gelöscht werden
3. Die einzelnen PDF-Dateien aus dem Report werden nach der E-Mail Adresse sortiert und in eine ZIP-Datei verpackt
    - CSV Datei mit Mapping IP auf E-Mail miteinbeziehen und die IP-Adressen mit den Namen der PDF-Dateien (uni_heidelberg_Medium_[IP Adresse].pdf) vergleichen 
    - Alle PDFs gruppiert nach den E-Mail Adressen werden in einen gemeinsamen Ordner ablegen
    - Daraus werden ZIP-Dateien erstellt ([IP-Adresse].zip)
    - Die ZIP Datei wird mit einem Passwort geschützt
4. Die Zip-Dateien werden in die Nextcloud geuploadet
    - Der Share der Nextcloud wird ebenfalls mit einem Passwort geschützt
    - Es wird ein Link erzeugt, der direkt zu der geuploadeten Datei führt
    - Der Link ist nur x Tage gültig
5. Es werden 2 One-Time-Links erstellt (https://onetimesecret.urz.uni-heidelberg.de:443)
    - Können nur einmal geöffnet werden 
    - Sichern die Kommunikation der Passwörter für die Nextcloud und für die ZIP-Datei ab
6. Es werden zwei verschiedene E-Mails versendet an einen Empfänger
    1. Enthält den Link zur Datei auf der Nextcloud + One-Time-Link der das Passwort für die ZIP-Datei enthält
    2. Enthält einen One-Time-Link der das Passwort für die Nextcloud enthält
7. Die Dateien auf der Nextcloud werden nach x Tagen gelöscht
    - Hierfür wurde ein Tag angelegt mit dem Namen "xxx"
    - Nach https://apps.nextcloud.com/apps/files_retention werden alle Dateien mit dem Tag "xxx" nach X Tagen gelöscht
