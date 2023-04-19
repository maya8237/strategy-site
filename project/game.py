# from db import get_db
import json
import os
from oauth2client.service_account import ServiceAccountCredentials
import googleapiclient.discovery
from google.oauth2 import service_account
from flask import request
from datetime import datetime
from dotenv import load_dotenv
import pytz

load_dotenv()

# RESEARCH ON SECURITY ON CLASS VARS
def get_form_data():
    cairo_tz = pytz.timezone('Africa/Cairo')
    now = datetime.now(tz=cairo_tz)
    tstamp = now.strftime("%d/%m/%Y %H:%M:%S")
    stats_to_get = ["timestamp", "scouter_name", "game_num", "team_num", "on_field", "starter_location",
                    "starter_tool_1", "starter_height_1", "starter_tool_2", "starter_height_2",
                    "starter_tool_3", "starter_height_3",
                    "auto_seesaw", "mobility",
                    "grid_co_h", "grid_co_m", "grid_co_l",
                    "grid_cu_h", "grid_cu_m", "grid_cu_l",
                    "cone_shoot", "cube_shoot",
                    "defence_execute", "defence_receive",
                    "dysfunction", "flip", "comments"]
    # TIMESTAMP
    stats_obtained = []
    for stat in stats_to_get:
        if stat == "timestamp":
            val = tstamp
        else:
            val = request.form.get(stat)
            print(f'{stat}:{val}')
        stats_obtained.append(val)
    Game(stats_obtained)
    return ("""<a style="font-family:calibri;text-align:center"/>
                <a href="/form" style="text-decoration:none;"><button type="button" style="
                width: 300px;
                font-size: 23px;
                border-radius: 5px;
                padding: 14px 25px;
                border: none;
                font-weight: 500;
                background-color: #5e1583;
                color: white;
                cursor: pointer;
                display: block;
                margin: auto;
                margin-top: 25px;">SUBMIT ANOTHER FORM</button></a>""")


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
    def is_data_in_sheet(self):
        service = get_service()
        range_name = 'Form Responses 1!B1:C'
        sheet_id = os.environ.get('GOOGLE_SPREADSHEET_ID')
        result = service.spreadsheets().values().get(
            spreadsheetId=sheet_id, range=range_name
        ).execute()
        existing_data = result.get('values', [])
        data = [self.stats[1], self.stats[2]]
        print(data)
        print(existing_data)
        return data in existing_data
    def upload_stats(self):
        stats = [self.stats]
        if self.is_data_in_sheet():
            print("FOUND DUPLICATE: "+str(self.stats))
            return None
        service = get_service()
        sheet_id = os.environ.get('GOOGLE_SPREADSHEET_ID')
        range_name = os.environ.get('GOOGLE_CELL_RANGE')
        result = service.spreadsheets().values().get(spreadsheetId=sheet_id, range=range_name).execute()
        num_rows = len(result.get('values', []))

        # Define the range to upload data to as the next empty row
        range_to_update = f'A{num_rows + 1}:AA'

        # Upload the values to the range
        body = {'values': stats}
        result = service.spreadsheets().values().update(spreadsheetId=sheet_id, range=range_to_update,
                                                        valueInputOption='USER_ENTERED', body=body).execute()
        print(f"{result.get('updatedCells')} cells updated.")

