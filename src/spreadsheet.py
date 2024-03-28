from __future__ import print_function

import pandas as pd

from GoogleService import GoogleService

goolgle_service = GoogleService()


def spreadsheet_range(spreadsheet_id, data_to_pull):
    result = goolgle_service.sheets_service.spreadsheets().values().get(spreadsheetId=spreadsheet_id,
                                                                        range=data_to_pull).execute()
    return result.get("values", [[None]])


def spreadsheet_cell(spreadsheet_id, cell):
    return spreadsheet_range(spreadsheet_id, cell)[0][0]


def spreadsheet_to_df(spreadsheet_id, data_to_pull):
    values = spreadsheet_range(spreadsheet_id, data_to_pull)

    if values:
        return pd.DataFrame(values[1:], columns=values[0])
    else:
        print("No data found.")


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
