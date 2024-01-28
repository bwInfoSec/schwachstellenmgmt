import smtplib
from datetime import datetime, timedelta

def read_email_body(file_path:str) -> str:
    """
    The method reads the email body from a text file

    Args:
    file_path (str): The path to the text file containing the email body.

    Returns:
    str: The content of the email body.

    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading email body from {file_path}: ", e)

def send_link_and_zipPassword_email(credentials:dict, receiver:str, nextcloud_file_url:str, zip_password_link:str, expiration_date: datetime, link_passwordZIP_emailText: str) -> None:
    """
    The method sends an email with a link to the file in the Nextcloud and a one-time secret link for the ZIP password.

    Args:
    credentials (dict): A dictionary containing access data for sending emails.
    receiver (str): The email address of the recipient.
    nextcloud_file_url (str): The URL of the file in the Nextcloud.
    zip_password_link (str): The one-time secret link for the ZIP password.
    expiration_date (datetime): The expiration date for the link.
    link_passwordZIP_emailText (str): The path to the text file containing the email template.

    Returns:
    None
    """
    
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

def send_NextcloudPassword_email(credentials: dict, receiver: str, nextcloud_password_link: str, passwordNextcloud_emailText:str) -> None:
    """
    The method sends an e-mail with a one-time link for the Nextcloud password

    Args:
    credentials (dict): A dictionary containing access data for sending emails.
    receiver (str): The email address of the recipient.
    nextcloud_password_link (str): The one-time secret link for the Nextcloud password.
    passwordNextcloud_emailText (str): The path to the text file containing the email template.

    Returns:
    None
    """
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
        
