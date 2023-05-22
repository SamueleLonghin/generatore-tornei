from __future__ import print_function

import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def spreadsheet_to_df(spreadsheet_id, data_to_pull):
    # creds = gsheet_api_check(SCOPES)
    credentials = service_account.Credentials.from_service_account_file('sa.json')
    service = build("sheets", "v4", credentials=credentials)
    sheet = service.spreadsheets()
    result = (
        sheet.values().get(spreadsheetId=spreadsheet_id, range=data_to_pull).execute()
    )
    values = result.get("values", [])

    if not values:
        print("No data found.")
    else:
        rows = (
            sheet.values()
            .get(spreadsheetId=spreadsheet_id, range=data_to_pull)
            .execute()
        )
        data = rows.get("values")
        return pd.DataFrame(data[1:], columns=data[0])


SPREADSHEET_ID = "1za3fWKC5tzrHgAarcRIPQVByM9ID5mXTzpLl-iI9Zsw"

RANGE_BEACH = "Beach"
RANGE_CALCETTO = "Calcetto"


def calcetto(limita=None):
    df = spreadsheet_to_df(SPREADSHEET_ID, RANGE_CALCETTO)
    if limita:
        df = df[:limita]
    return df


def beach(limita=None):
    df = spreadsheet_to_df(SPREADSHEET_ID, RANGE_BEACH)
    if limita:
        df = df[:limita]
    return df
