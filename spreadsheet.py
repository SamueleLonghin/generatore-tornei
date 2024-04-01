from __future__ import print_function

import pandas as pd

from GoogleService import GoogleService
from secret import RANGE_CALCETTO, RANGE_BEACH, SPREADSHEET_ID

goolgle_service = GoogleService()


def spreadsheet_name(spreadsheet_id):
    return goolgle_service.drive_service.files().get(fileId=spreadsheet_id, fields='name').execute()['name']


def spreadsheet_range(spreadsheet_id, data_to_pull):
    result = goolgle_service.sheets_service.spreadsheets().values().get(spreadsheetId=spreadsheet_id,
                                                                        range=data_to_pull).execute()
    return result.get("values", [[None]])


def spreadsheet_cell(spreadsheet_id, cell, default=""):
    value = spreadsheet_range(spreadsheet_id, cell)[0][0]
    return value if value else default


def spreadsheet_to_df(spreadsheet_id, data_to_pull):
    values = spreadsheet_range(spreadsheet_id, data_to_pull)

    if values:
        return pd.DataFrame(values[1:], columns=values[0])
    else:
        print("No data found.")


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
