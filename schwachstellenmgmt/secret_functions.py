import requests
import secrets

def generate_random_password(length=12) -> str:
    """
    The method generates a random password

    Args:
    length (int): The length of the generated password.

    Returns:
    str: The generated random password.
    """
    try:
        return secrets.token_urlsafe(length)
    except Exception as e:
        print(f"Error generating random password: ", e)

def create_one_time_secret_link(secret: str, credentials: dict) -> str:
    """
    The function creates a one-time link for the submitted secret with a custom URL for Heidelberg University's One-Time Secret service

    Args:
    secret (str): The secret for which the one-time link is generated.
    credentials (dict): A dictionary containing access data for creating the one-time link.

    Returns:
    str: The generated one-time link.
    """

    try:
        otp_domain = credentials['otp_domain']

        # Send request to create the one-time secret to the One-Time-Secret API
        response = requests.post(otp_domain + '/api/v1/share', data={'secret': secret})
        response_data = response.json()

        secret_key = response_data['secret_key']

        # Create the one-time link
        link = otp_domain + '/secret/' + secret_key
        return link

    except Exception as e:
        print(f"Error creating one-time link: ", e)
