from google.oauth2 import service_account
from googleapiclient.discovery import build

from config import SERVICE_ACCOUNT_SCOPES, SERVICE_ACCOUNT_CREDENTIALS


class GoogleService:
    def __init__(self):
        self.credentials_file = SERVICE_ACCOUNT_CREDENTIALS
        self.scopes = SERVICE_ACCOUNT_SCOPES
        self.credentials = service_account.Credentials.from_service_account_file(self.credentials_file,
                                                                                 scopes=self.scopes)
        self.sheets_service = build("sheets", "v4", credentials=self.credentials)
        self.drive_service = build('drive', 'v3', credentials=self.credentials)
