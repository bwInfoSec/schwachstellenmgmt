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
        
    
# Function to read the email body from a text file
def read_email_body(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading email body from {file_path}: {str(e)}")
        return ""

# The function sends an e-mail with a one-time link for the share password
def send_NextcloudPassword_email(receiver, subject, nextcloud_password_link, passwordNextcloud_emailText):
    try:
        credentials = read_smtp_credentials()
        email_body = read_email_body(passwordNextcloud_emailText)

        if email_body:
            message = f"""\
Subject: {subject}
To: {receiver}
From: {credentials['SMTP_email']}

{email_body.format(nextcloud_password_link=nextcloud_password_link)}
"""

            # Establish SMTP connection and send email
            with smtplib.SMTP(credentials['SMTP_domain'], int(credentials['SMTP_port'])) as server:
                server.login(credentials['SMTP_username'], credentials['SMTP_password'])
                server.sendmail(credentials['SMTP_email'], receiver, message.encode('utf-8'))
    except Exception as e:
        print(f"Error sending share password email: {str(e)}")

# The function sends an email with a link and a one-time secret link for the ZIP password
def send_link_and_zipPassword_email(receiver, subject, nextcloud_file_url, zip_password_link, expiration_date, link_passwordZIP_emailText):
    try:
        credentials = read_smtp_credentials()
        email_body = read_email_body(link_passwordZIP_emailText)

        if email_body:
            message = f"""\
Subject: {subject}
To: {receiver}
From: {credentials['SMTP_email']}

{email_body.format(nextcloud_file_url=nextcloud_file_url, zip_password_link=zip_password_link, expiration_date=expiration_date)}
"""

            # Establish SMTP connection and send email
            with smtplib.SMTP(credentials['SMTP_domain'], int(credentials['SMTP_port'])) as server:
                server.login(credentials['SMTP_username'], credentials['SMTP_password'])
                server.sendmail(credentials['SMTP_email'], receiver, message.encode('utf-8'))
    except Exception as e:
        print(f"Error sending link and ZIP password email: {str(e)}")
        
