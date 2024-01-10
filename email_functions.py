import smtplib

# The function reads SMTP credentials from the credentials.txt file
def read_smtp_credentials():
    try:
        with open('credentials.txt', 'r') as file:
            lines = file.readlines()
            credentials = {}
            for line in lines:
                key, value = line.strip().split('=')
                credentials[key] = value
            return credentials
    except Exception as e:
        print(f"Error reading SMTP credentials: {str(e)}")
        
    
# The function sends an e-mail with a one-time link for the share password
def send_sharePassword_email(receiver, subject, share_password_link):
    try:
        credentials = read_smtp_credentials()

        message = f"""\
Subject: {subject}
To: {receiver}
From: {credentials['SMTP_email']}

{f"""\
English version below!
 
Sehr geehrte Damen und Herren,

innerhalb der Universität Heidelberg wurde durch das Universitätsrechenzentrum ein Scan durchgeführt, der wichtige Informationen über die vorhandenen und verwendeten IP-Adressen lieferte. Hier besteht dringender Handlungsbedarf.
In einer vorherigen E-Mail haben Sie bereits einen Link zu einer Datei enthalten, welche die wichtigsten Informationen zusammenfasst. Der Speicherort dieser Datei ist jedoch mit einem Passwort geschützt, welches Sie unter folgendem einmaligem Link finden können:
{share_password_link}

Mit freundlichen Grüßen,
URZ


__________________________________________________________

Dear Sir or Madam,

A scan was carried out within Heidelberg University by the University Computer Center, which provided important information about the available IP addresses. There is an urgent need for action here.
In a previous e-mail you have already included a link to a file which summarizes the most important information. However, the storage location of this file is protected with a password, which you can find under the following unique link:
{share_password_link}

Yours sincerely, 
URZ
"""
}"""       

        # Establish SMTP connection and send email
        with smtplib.SMTP(credentials['SMTP_domain'], int(credentials['SMTP_port'])) as server:
            server.login(credentials['SMTP_username'], credentials['SMTP_password'])
            server.sendmail(credentials['SMTP_email'], receiver, message.encode('utf-8'))
    except Exception as e:
        print(f"Error sending share password email: {str(e)}")
        

# The function sends an email with a link and a one-time secret link for the ZIP password
def send_link_and_zipPassword_email(receiver, subject, share_url, zip_password_link, expiration_date):
    try:
        credentials = read_smtp_credentials()
        
        message = f"""\
Subject: {subject}
To: {receiver}
From: {credentials['SMTP_email']}

{f"""\
English version below!

Sehr geehrte Damen und Herren,

innerhalb der Universität Heidelberg wurde durch das Universitätsrechenzentrum ein Scan durchgeführt, der wichtige Informationen über die vorhandenen und verwendeten IP-Adressen lieferte. Hier besteht dringender Handlungsbedarf. 
Die Ergebnisse des Scans und die empfohlene Lösung des Problems finden Sie in einer Zip-Datei unter folgendem Link: 
{share_url}
(Bitte beachten Sie, dass der Link nur bis {expiration_date} gültig ist)

Um die Sicherheit zu erhöhen, ist der Zugriff auf den Speicherort der Zip-Datei mit einem Passwort geschützt. Das Passwort hierfür finden Sie in einer separaten E-Mail. 

Auch die Zip-Datei ist mit einem Passwort geschützt, das Sie mit dem folgenden einmaligen Link aufrufen können:
{zip_password_link}
(Die Zip-Datei lässt sich mit dem Programm 7-Zip File Manager entpacken und entschlüsseln)

Bei Fragen wenden Sie sich bitte an die folgende E-Mail-Adresse: URZ_EMAIL

Mit freundlichen Grüßen, 
URZ
__________________________________________________________

Dear Sir or Madam,

A scan was carried out within Heidelberg University by the University Computer Center, which provided important information about the IP addresses available and in use. There is an urgent need for action here. 
The results of the scan and the recommended solution to the problem can be found in a zip file under the following link: 
{share_url}
(Please note that the link is only valid until {expiration_date})

To increase security, access to the storage location of the zip file is protected with a password. You will find the password for this in a separate e-mail. 

Also the zip file is password protected and can be accessed using the following unique link:
{zip_password_link}
(The zip file can be unpacked and decrypted using the 7-Zip File Manager program)


If you have any questions, please contact the following e-mail address: URZ_EMAIL

Yours sincerely, 
URZ


"""
}"""

        # Establish SMTP connection and send email
        with smtplib.SMTP(credentials['SMTP_domain'], int(credentials['SMTP_port'])) as server:
            server.login(credentials['SMTP_username'], credentials['SMTP_password'])
            server.sendmail(credentials['SMTP_email'], receiver, message.encode('utf-8'))
    except Exception as e:
        print(f"Error sending link and ZIP password email: {str(e)}")
        
