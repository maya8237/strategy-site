import json
import os
from oauth2client.service_account import ServiceAccountCredentials
import googleapiclient.discovery
from google.oauth2 import service_account
from flask import request
from datetime import datetime
from dotenv import load_dotenv
import pytz
from app import db
from sheets_api import *
from models import GameData
# from .game_model import GameData
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
            print(f'{stat}:{val}') # DONT PRINT
        stats_obtained.append(val)
    game = Game(stats_obtained)
    return game


# tal haker was here :)
class Game:
    def __init__(self, stats):
        self.stats = stats
        self.game_data = GameData(stats)
        self.upload_stats()
        self.game_data.add_to_game_db()

    def delete_game(self): # MAYAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        pass


    def is_data_in_sheet(self):
        # check in database if there are dupes
        return False

    def upload_stats(self):
        stats = [self.stats]
        if self.is_data_in_sheet():
            print("FOUND DUPLICATE: "+str(self.stats))  # DONT PRINT
            return None
        service = get_service()
        sheet_id = os.environ.get('GOOGLE_SPREADSHEET_ID')

        # Get number of rows with text
        checking_range_name = os.environ.get('GOOGLE_CHECKING_RANGE')
        result = service.spreadsheets().values().get(spreadsheetId=sheet_id, range=checking_range_name).execute()
        num_rows = len(result.get('values', []))

        # Define the range to upload data to as the next empty row
        range_to_update = f'A{num_rows + 1}:AA'

        # Upload the values to the range
        body = {'values': stats}
        result = service.spreadsheets().values().update(spreadsheetId=sheet_id, range=range_to_update,
                                                        valueInputOption='USER_ENTERED', body=body).execute()
        print(f"{result.get('updatedCells')} cells updated.")

