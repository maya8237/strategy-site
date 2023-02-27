from db import get_db
import json
import os
from oauth2client.service_account import ServiceAccountCredentials
import googleapiclient.discovery
from google.oauth2 import service_account
from flask import request
from datetime import datetime


# RESEARCH ON SECURITY ON CLASS VARS
def get_form_data():
    now = datetime.now()
    tstamp = now.strftime("%d/%m/%Y %H:%M:%S")
    stats_to_get = ["timestamp", "scouter_name", "game_num", "team_num", "start_location",
                    "auto_o", "auto_a", "auto_b", "auto_c", "auto_d",
                    "auto_drop", "auto_seesaw", "mobility", 
                    "grid_h", "grid_m", "grid_lc", "grid_lf", "tele_drop", "tele_intake",
                    "defence_execute", "defence_location", "defence_receive", "intake_cones",
                    "intake_floats", "zone_foul", "seesaw_go_over", "endgame_seesaw",
                    "endgame_num", "disfunction", "comments"]
    form_vals = ["timestamp", "scouter_name", "game_num", "team_num"]
    # TIMESTAMP
    stats_obtained = []
    for stat in stats_to_get:
        if stat == "timestamp":
            val = tstamp
        else:
            if stat in form_vals:
                val = request.form.get(stat)
            else:
                val = None
        stats_obtained.append(val)
    Game(stats_obtained)
    return ('<h1 style="font-family:calibri;text-align:center">'
            '<a class="button" href="/form">SUBMIT ANOTHER FORM</a></h1>')


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
    def __init__(self, stats):
        # self.get_values()
        # self.stats = [game_num, game_type, team_num, scouter_name]
        # self.put_into_db(stats)
        self.stats = stats
        self.upload_stats()

    def put_into_db(self):
        db = get_db()
        db.execute(
            """INSERT INTO games (team_num, game_num, game_type,
                 scouter_name) """
            "VALUES (?, ?, ?, ?)",
            (team_num, game_num, game_type,
             scouter_name),
        )
        db.commit()

    def upload_stats(self):
        stats = [self.stats]
        service = get_service()
        sheet_id = os.environ.get('GOOGLE_SPREADSHEET_ID')
        range_name = os.environ.get('GOOGLE_CELL_RANGE')
        result = service.spreadsheets().values().get(spreadsheetId=sheet_id, range=range_name).execute()
        num_rows = len(result.get('values', []))

        # Define the range to upload data to as the next empty row
        range_to_update = f'A{num_rows + 1}:AE'

        # Upload the values to the range
        body = {'values': stats}
        result = service.spreadsheets().values().update(spreadsheetId=sheet_id, range=range_to_update,
                                                        valueInputOption='USER_ENTERED', body=body).execute()
        print(f"{result.get('updatedCells')} cells updated.")
