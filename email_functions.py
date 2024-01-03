import smtplib

# The function sends an email from the sender to the recipient
# The email contains a message with a one-time-secret link for the Nextcloud share password
# TODO body
def send_sharePassword_email(sender, receiver, subject, share_password_link):
    message = f"""\
Subject: {subject}
To: {receiver}
From: {sender}

{f"""\
One-Time-Secret Link for Share Password: {share_password_link}."""
}"""       

    SMTP_domain = "domain.org"
    SMTP_port = 1234
    SMTP_username = "USERNAME"
    SMTP_password = "PASSWORD"

    with smtplib.SMTP(SMTP_domain, SMTP_port) as server:
        server.login(SMTP_username, SMTP_password)
        server.sendmail(sender, receiver, message)


# The function sends an email from the sender to the recipient
# The email contains a message with a link and a one-time secret link for the ZIP password
# TODO body
def send_link_and_zipPassword_email(sender, receiver, subject,share_url,zip_password_link):
    message = f"""\
Subject: {subject}
To: {receiver}
From: {sender}

{f"""\
Share Link: {share_url}
One-Time-Secret Link for ZIP Password: {zip_password_link}"""
}"""
    SMTP_domain = "domain.org"
    SMTP_port = 1234
    SMTP_username = "USERNAME"
    SMTP_password = "PASSWORD"

    with smtplib.SMTP(SMTP_domain, SMTP_port) as server:
        server.login(SMTP_username, SMTP_password)
        server.sendmail(sender, receiver, message)
