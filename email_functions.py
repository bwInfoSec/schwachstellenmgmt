import smtplib
import os

# The function reads SMTP credentials from the credentials.txt file
def read_smtp_credentials():
    with open('credentials.txt', 'r') as file:
        lines = file.readlines()
        credentials = {}
        for line in lines:
            key, value = line.strip().split('=')
            credentials[key] = value
        return credentials

# The function sends an email with a one-time secret link for the share password
def send_sharePassword_email(receiver, subject, share_password_link):
    # Read SMTP credentials from the credentials.txt file
    credentials = read_smtp_credentials()

    # Create email message
    message = f"""\
Subject: {subject}
To: {receiver}
From: {credentials['email']}

{f"""\
One-Time-Secret Link for Share Password: {share_password_link}."""
}"""       

    # Establish SMTP connection and send email
    with smtplib.SMTP(credentials['SMTP_domain'], int(credentials['SMTP_port'])) as server:
        server.login(credentials['SMTP_username'], credentials['SMTP_password'])
        server.sendmail(credentials['email'], receiver, message)

# The function sends an email with a link and a one-time secret link for the ZIP password
def send_link_and_zipPassword_email(receiver, subject, share_url, zip_password_link):
    # Read SMTP credentials from the credentials.txt file
    credentials = read_smtp_credentials()

    # Create email message
    message = f"""\
Subject: {subject}
To: {receiver}
From: {credentials['email']}

{f"""\
Share Link: {share_url}
One-Time-Secret Link for ZIP Password: {zip_password_link}"""
}"""

    # Establish SMTP connection and send email
    with smtplib.SMTP(credentials['SMTP_domain'], int(credentials['SMTP_port'])) as server:
        server.login(credentials['SMTP_username'], credentials['SMTP_password'])
        server.sendmail(credentials['email'], receiver, message)
