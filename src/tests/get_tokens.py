import os
from os.path import dirname, abspath
import random
import json
import requests
from dotenv import load_dotenv

basedir = dirname(dirname(abspath(__file__)))

load_dotenv(os.path.join(basedir, '.env'))


def get_auth_token_from_Auth0(client_id=None, client_secret=None):
    """
    This returns an auth0 token for the provided login credentials
    """

    AUTH0_TENANT_DOMAIN = os.getenv('AUTH0_TENANT_DOMAIN')

    url = f'https://{AUTH0_TENANT_DOMAIN}/oauth/token'

    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "audience": os.getenv('AUTH0_API_AUDIENCE'),
        "grant_type": "client_credentials"
    }

    response_object = requests.post(url=url, json=payload)

    response_data = response_object.json()

    if "access_token" in response_data and "token_type" in response_data:
        return response_data['access_token']

    return None


admin_client_id = os.getenv('TEST_ADMIN_CLIENT_ID')
admin_client_secret = os.getenv('TEST_ADMIN_CLIENT_SECRET')

student_client_id = os.getenv('TEST_STUDENT_CLIENT_ID')
student_client_secret = os.getenv('TEST_STUDENT_CLIENT_SECRET')


admin_token = get_auth_token_from_Auth0(
    client_id=admin_client_id, client_secret=admin_client_secret)

student_token = get_auth_token_from_Auth0(
    client_id=student_client_id, client_secret=student_client_secret)

tokens = {
    "admin_token": admin_token,
    "student_token": student_token
}


with open('tokens.txt', 'w') as outfile:
    json.dump(tokens, outfile)
