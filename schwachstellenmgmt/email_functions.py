import smtplib
from datetime import datetime, timedelta

# The function reads the email body from a text file
def read_email_body(file_path:str) -> str:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading email body from {file_path}: ", e)

# The function sends an email with a link to the file in the Nextcloud and a one-time secret link for the ZIP password
def send_link_and_zipPassword_email(credentials:dict, receiver:str, nextcloud_file_url:str, zip_password_link:str, expiration_date: datetime, link_passwordZIP_emailText: str) -> None:
    try:
        email_body = read_email_body(link_passwordZIP_emailText)

        if email_body:
            message = f"""\
Subject: Security Vulnerability Scan Report - (Nextcloud Link and ZIP Password)
To: {receiver}
From: {credentials['SMTP_email']}

{email_body.format(nextcloud_file_url=nextcloud_file_url, zip_password_link=zip_password_link, expiration_date=expiration_date)}
"""
            # Create SMTP connection and send email
            with smtplib.SMTP(credentials['SMTP_domain'], int(credentials['SMTP_port'])) as server:
                server.login(credentials['SMTP_username'], credentials['SMTP_password'])
                server.sendmail(credentials['SMTP_email'], receiver, message.encode('utf-8'))
    except Exception as e:
        print(f"Error sending link and ZIP password email: ", e)

# The function sends an e-mail with a one-time link for the Nextcloud password
def send_NextcloudPassword_email(credentials: dict, receiver: str, nextcloud_password_link: str, passwordNextcloud_emailText:str) -> None:
    try:
        email_body = read_email_body(passwordNextcloud_emailText)

        if email_body:
            message = f"""\
Subject: Security Vulnerability Scan Report - (Nextcloud Password)
To: {receiver}
From: {credentials['SMTP_email']}

{email_body.format(nextcloud_password_link=nextcloud_password_link)}
"""

            # Create SMTP connection and send email
            with smtplib.SMTP(credentials['SMTP_domain'], int(credentials['SMTP_port'])) as server:
                server.login(credentials['SMTP_username'], credentials['SMTP_password'])
                server.sendmail(credentials['SMTP_email'], receiver, message.encode('utf-8'))
    except Exception as e:
        print(f"Error sending share password email: ", e)
        
