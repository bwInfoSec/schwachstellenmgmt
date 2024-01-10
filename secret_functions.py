import requests
import secrets

# The function reads One-Time-Secret credentials from the credentials.txt file
def read_onetimesecret_credentials():
    try:
        with open('credentials.txt', 'r') as file:
            lines = file.readlines()
            credentials = {}
            for line in lines:
                key, value = line.strip().split('=')
                credentials[key] = value
            return credentials
    except Exception as e:
        print(f"Error reading One-Time-Secret credentials: {str(e)}")

# The function generates a random password with a default length of 12 characters
def generate_random_password(length=12):
    try:
        return secrets.token_urlsafe(length)
    except Exception as e:
        print(f"Error generating random password: {str(e)}")

# The function creates a one-time secret link for the submitted secret 
# with a custom URL for Heidelberg University's One-Time Secret service
def create_one_time_secret_link(secret):
    try:
        # Read One-Time-Secret credentials from the credentials.txt file
        credentials = read_onetimesecret_credentials()
        otp_domain = credentials['otp_domain']

        # Send request to create the one-time secret to the One-Time-Secret API
        response = requests.post(otp_domain + '/api/v1/share', data={'secret': secret})
        response_data = response.json()

        secret_key = response_data['secret_key']

        # Create the one-time secret link
        link = otp_domain + '/secret/' + secret_key
        return link

    except Exception as e:
        print(f"Error creating One-Time-Secret link: {str(e)}")