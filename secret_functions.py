from onetimesecret import OneTimeSecretCli
import secrets
import os

# The function reads One-Time-Secret credentials from the credentials.txt file
def read_onetimesecret_credentials():
    with open('credentials.txt', 'r') as file:
        lines = file.readlines()
        credentials = {}
        for line in lines:
            key, value = line.strip().split('=')
            credentials[key] = value
        return credentials

# The function generates a random password with a default length of 12 characters
def generate_random_password(length=12):
    return secrets.token_urlsafe(length)

# The function creates a one-time secret link for the submitted secret 
# with a specific email, API key, and custom URL for Heidelberg University's One-Time Secret service
def create_one_time_secret_link(secret):
    # Read One-Time-Secret credentials from the credentials.txt file
    credentials = read_onetimesecret_credentials()

    email = credentials['email']
    api_key = credentials['api_key']
    custom_url = credentials['custom_url']

    oneTimeSecretCli = OneTimeSecretCli(email, api_key, url=custom_url)
    return oneTimeSecretCli.create_link(secret)
