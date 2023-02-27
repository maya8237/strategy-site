from db import get_db
import json
import os
from oauth2client.service_account import ServiceAccountCredentials
import googleapiclient.discovery
from google.oauth2 import service_account
# RESEARCH ON SECURITY ON CLASS VARS

def get_form_data():
    pass
def get_credentials():
    scopes = ['https://www.googleapis.com/auth/spreadsheets']
    GOOGLE_PRIVATE_KEY = os.environ.get('GOOGLE_PRIVATE_KEY', None)
    account_info = {
        "private_key": GOOGLE_PRIVATE_KEY,
        "client_email": os.environ.get('GOOGLE_CLIENT_EMAIL'),
        "token_uri": "https://accounts.google.com/o/oauth2/token",
    }

    credentials = service_account.Credentials.from_service_account_info(account_info, scopes=scopes)
    return credentials


def get_service(service_name='sheets', api_version='v4'):
    credentials = get_credentials()
    service = googleapiclient.discovery.build(service_name, api_version, credentials=credentials)
    return service

# tal haker was here :)
class Game:
    def __init__(self, scouter_name, game_num, team_num
                 ):
        db = get_db()
        db.execute(
            """INSERT INTO games (team_num, game_num, game_type,
                 scouter_name) """
            "VALUES (?, ?, ?, ?)",
            (team_num, game_num, game_type,
             scouter_name),
        )
        db.commit()
        # self.get_values()
        stats = [[game_num, game_type, team_num, scouter_name]]
        self.upload_stats(stats)

    def upload_stats(self, stats):
        service = get_service()
        sheet_id = os.environ.get('GOOGLE_SPREADSHEET_ID')
        range_name = os.environ.get('GOOGLE_CELL_RANGE')
        result = service.spreadsheets().values().get(spreadsheetId=sheet_id, range=range_name).execute()
        num_rows = len(result.get('values', []))

        # Define the range to upload data to as the next empty row
        range_to_update = f'A{num_rows + 1}:AG'

        # Upload the values to the range
        body = {'values': stats}
        result = service.spreadsheets().values().update(spreadsheetId=sheet_id, range=range_to_update,
                                                        valueInputOption='USER_ENTERED', body=body).execute()
        print(f"{result.get('updatedCells')} cells updated.")

