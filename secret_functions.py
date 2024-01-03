from onetimesecret import OneTimeSecretCli
import secrets

# The function generates a random password with a standard length of 12 characters #TODO 12?
def generate_random_password(length=12):
    return secrets.token_urlsafe(length)

# The function "create_one_time_secret_link" creates a one-time secret link for the submitted secret 
# with a specific email, API key and custom URL for Heidelberg University's One-Time Secret service
def create_one_time_secret_link(secret):
    email = "EMAIL"  
    api_key = "API_KEY"  
    custom_url = "https://onetimesecret.urz.uni-heidelberg.de:443"  

    oneTimeSecretCli = OneTimeSecretCli(email, api_key, url=custom_url)
    return oneTimeSecretCli.create_link(secret)
