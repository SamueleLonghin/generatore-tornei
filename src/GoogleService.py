from google.oauth2 import service_account
from googleapiclient.discovery import build

from src.config import SERVICE_ACCOUNT_SCOPES, SERVICE_ACCOUNT_CREDENTIALS, BASE_FOLDER, SHEET_NAME, SPREADSHEET_NAME, \
    ORIGINAL_SPREADSHEET_ID


class GoogleService:
    def __init__(self):
        self.credentials_file = SERVICE_ACCOUNT_CREDENTIALS
        self.scopes = SERVICE_ACCOUNT_SCOPES
        self.credentials = service_account.Credentials.from_service_account_file(self.credentials_file,
                                                                                 scopes=self.scopes)
        self.sheets_service = build("sheets", "v4", credentials=self.credentials)
        self.drive_service = build('drive', 'v3', credentials=self.credentials)

    def create_spreadsheet(self, title=SPREADSHEET_NAME):
        # spreadsheet = self.sheets_service.spreadsheets().create(body={
        #     'properties': {'title': title},
        #     'sheets': [
        #         {
        #             'properties': {
        #                 'title': SHEET_NAME,
        #             }
        #         }
        #     ]
        # }).execute()

        copied_file = {'name': title, 'parents': [BASE_FOLDER]}

        file = self.drive_service.files().copy(
            fileId=ORIGINAL_SPREADSHEET_ID,
            body=copied_file,
        ).execute()

        print(file)
        return file['id']

        # self.drive_service.files().update(
        #     fileId=spreadsheet['spreadsheetId'],
        #     addParents=BASE_FOLDER,
        #     removeParents='root',
        #     fields='id, parents'
        # ).execute()

        # return spreadsheet['spreadsheetId']

    def share_spreadsheet(self, spreadsheet_id):
        self.drive_service.permissions().create(
            fileId=spreadsheet_id,
            body={'type': 'anyone', 'role': 'writer'},
            fields='id'
        ).execute()
