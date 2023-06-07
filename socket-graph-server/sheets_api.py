import os
from oauth2client.service_account import ServiceAccountCredentials
import googleapiclient.discovery
from google.oauth2 import service_account
from dotenv import load_dotenv


def get_credentials():
    load_dotenv()
    PRIVATE_KEY = os.environ.get('GOOGLE_PRIVATE_KEY', None)
    CLIENT_EMAIL = os.environ.get('SOCKET_CLIENT_EMAIL')
    scopes = ['https://www.googleapis.com/auth/spreadsheets']
    account_info = {
        "private_key": PRIVATE_KEY,
        "client_email": CLIENT_EMAIL,
        "token_uri": "https://accounts.google.com/o/oauth2/token",
    }

    credentials = service_account.Credentials.from_service_account_info(account_info, scopes=scopes)
    return credentials


def get_service(service_name='sheets', api_version='v4'):
    credentials = get_credentials()
    service = googleapiclient.discovery.build(service_name, api_version, credentials=credentials)
    return service
