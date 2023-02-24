from db import get_db
import json
import os
from oauth2client.service_account import ServiceAccountCredentials
import googleapiclient.discovery
from google.oauth2 import service_account
# RESEARCH ON SECURITY ON CLASS VARS

def get_credentials():
    scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
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
    def __init__(self, game_num, game_type, team_num,
                 scouter_name):
        db = get_db()
        db.execute(
            """INSERT INTO games (team_num, game_num, game_type,
                 scouter_name) """
            "VALUES (?, ?, ?, ?)",
            (team_num, game_num, game_type,
             scouter_name),
        )
        db.commit()
        self.get_values()
        # self.id = id_
        # self.game_num = game_num
        # self.game_type = game_type
        # self.team_num = team_num
        # self.form_filler = form_filler
        # self.auto_climb_lvl = auto_climb_lvl
        # self.auto_balls_amt = auto_balls_amt
        # self.create()

    def get_values(self):
        service = get_service()
        spreadsheet_id = os.environ.get('GOOGLE_SPREADSHEET_ID')
        range_name = os.environ.get('GOOGLE_CELL_RANGE')

        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range=range_name).execute()
        values = result.get('values', [])
        print(values)
    # def to_sheets(self):
    #     """Shows basic usage of the Sheets API.
    #     Prints values from a sample spreadsheet.
    #     """
    #     creds = None
    #     # The file token.json stores the user's access and refresh tokens, and is
    #     # created automatically when the authorization flow completes for the first
    #     # time.
    #     if os.path.exists('token.json'):
    #         creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    #     # If there are no (valid) credentials available, let the user log in.
    #     if not creds or not creds.valid:
    #         if creds and creds.expired and creds.refresh_token:
    #             creds.refresh(Request())
    #         else:
    #             flow = InstalledAppFlow.from_client_secrets_file(
    #                 'credentials.json', SCOPES)
    #             creds = flow.run_local_server(port=0)
    #         # Save the credentials for the next run
    #         with open('token.json', 'w') as token:
    #             token.write(creds.to_json())
    #
    #     try:
    #         service = build('sheets', 'v4', credentials=creds)
    #
    #         # Call the Sheets API
    #         sheet = service.spreadsheets()
    #         result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
    #                                     range=SAMPLE_RANGE_NAME).execute()
    #         values = result.get('values', [])
    #
    #         if not values:
    #             print('No data found.')
    #             return
    #
    #         print('Name, Major:')
    #         for row in values:
    #             # Print columns A and E, which correspond to indices 0 and 4.
    #             print('%s, %s' % (row[0], row[4]))
    #     except HttpError as err:
    #         print(err)

    #@staticmethod
    #def get(game_type, game_num):
    #    db = get_db()
        # user = db.execute(
        #     "SELECT * FROM user WHERE id = ?", (user_id,)
        # ).fetchone()
        # if not user:
        #     return None
        #
        # user = User(
        #     id_=user[0], name=user[1], email=user[2], profile_pic=user[3]
        # )
        # return user

    # def create(self):
    #     db = get_db()
    #     db.execute(
    #         """INSERT INTO games (id, team_num, game_num, game_type,
    #              form_filler, auto_climb_lvl, auto_balls_amt) """
    #         "VALUES (?, ?, ?, ?, ?, ?, ?)",
    #         (self.id, self.team_num, self.game_num, self.game_type,
    #          self.form_filler, self.auto_climb_lvl, self.auto_balls_amt),
    #     )
    #     db.commit()
