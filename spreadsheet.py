import pandas as pd

from GoogleService import GoogleService
from config import ORIGINAL_SPREADSHEET_ID, BASE_FOLDER, SPREADSHEET_NAME, TEAMS_SHEET_NAME, RANGE_TEAM_NAMES
from secret import RANGE_CALCETTO, RANGE_BEACH, SPREADSHEET_ID

goolgle_service = GoogleService()


def create_spreadsheet(title=SPREADSHEET_NAME):
    spreadsheet = goolgle_service.sheets_service.spreadsheets().create(body={
        'properties': {'title': title},
        'sheets': [
            {
                'properties': {
                    'title': TEAMS_SHEET_NAME,
                }
            }
        ]
    }).execute()
    goolgle_service.drive_service.files().update(
        fileId=spreadsheet['spreadsheetId'],
        addParents=BASE_FOLDER,
        removeParents='root',
        fields='id, parents'
    ).execute()

    return spreadsheet['spreadsheetId']


def create_sheet(spreadsheet_id, name, prec=[]):
    requests = [
        *prec,
        {
            "addSheet": {
                "properties": {
                    "title": name,  # Il nome del nuovo foglio
                    "gridProperties": {
                        "rowCount": 1000,  # Numero di righe
                        "columnCount": 5  # Numero di colonne
                    },
                    "tabColor": {
                        "red": 1.0,  # Valori RGB tra 0 e 1 per il colore del tab
                        "green": 0.3,
                        "blue": 0.4
                    }
                }
            }
        }
    ]

    # Invio della richiesta batchUpdate per aggiungere il nuovo foglio
    body = {
        'requests': requests
    }
    response = goolgle_service.sheets_service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id,
                                                                         body=body).execute()
    return response


def create_sheet_if_not_exists(spreadsheet_id, name):
    # Ottieni le informazioni sullo Spreadsheet, inclusi i fogli
    spreadsheet_info = goolgle_service.sheets_service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()

    # Estrai l'elenco dei fogli (sheets) presenti nello Spreadsheet
    sheets = spreadsheet_info.get('sheets', '')

    # Controlla se il foglio specificato esiste
    if not any(sheet['properties']['title'] == name for sheet in sheets):
        result = create_sheet(spreadsheet_id, name)
    else:
        sheet_id = None
        for sheet in sheets:
            if sheet['properties']['title'] == name:
                sheet_id = sheet['properties']['sheetId']
                break
        delete = {
            "deleteSheet": {
                "sheetId": sheet_id
            }
        }
        result = create_sheet(spreadsheet_id, name, [delete])

    # Scorro le risposte e ottengo l'id del nuovo foglio
    for reply in result['replies']:
        if 'addSheet' in reply:
            sheet_id = reply['addSheet']['properties']['sheetId']
            return sheet_id


def clone_spreadsheet(title=SPREADSHEET_NAME):
    copied_file = {'name': title, 'parents': [BASE_FOLDER]}

    file = goolgle_service.drive_service.files().copy(
        fileId=ORIGINAL_SPREADSHEET_ID,
        body=copied_file,
    ).execute()

    print(file)
    return file['id']


def share_spreadsheet(spreadsheet_id):
    goolgle_service.drive_service.permissions().create(
        fileId=spreadsheet_id,
        body={'type': 'anyone', 'role': 'writer'},
        fields='id'
    ).execute()


def spreadsheet_name(spreadsheet_id):
    return goolgle_service.drive_service.files().get(fileId=spreadsheet_id, fields='name').execute()['name']


def spreadsheet_range(spreadsheet_id, data_to_pull):
    result = goolgle_service.sheets_service.spreadsheets().values().get(spreadsheetId=spreadsheet_id,
                                                                        range=data_to_pull).execute()
    return result.get("values", [[None]])


def spreadsheet_cell(spreadsheet_id, cell, default=""):
    value = spreadsheet_range(spreadsheet_id, cell)[0][0]
    return value if value else default


def spreadsheet_to_df(spreadsheet_id, data_to_pull=TEAMS_SHEET_NAME + RANGE_TEAM_NAMES):
    values = spreadsheet_range(spreadsheet_id, data_to_pull)

    if values:
        return pd.DataFrame(values[1:], columns=values[0])
    else:
        print("No data found.")


def df_to_spreadsheet(spreadsheet_id, data_range, df: pd.DataFrame):
    values = [df.columns.values.tolist()] + df.values.tolist()

    writeCells(spreadsheet_id, data_range, values)
    #
    # body = {
    #     'values': values
    # }
    # result = goolgle_service.sheets_service.spreadsheets().values().update(
    #     spreadsheetId=spreadsheet_id,
    #     range=data_range,
    #     valueInputOption='RAW',
    #     body=body
    # ).execute()
    # return result


def mergeCells(data_range):
    return {
        "mergeCells": {
            "range": data_range,
            "mergeType": "MERGE_ALL"
        }
    }


def setTextFormat(data_range, font_size=None, bold=None, **kwargs):
    """
    Imposta la dimensione del carattere e il grassetto per un range di celle.

    Args:
    - font_size (int): Dimensione del carattere da impostare.
    - bold (bool): True per impostare il testo in grassetto, False altrimenti.
    """
    return {
        "repeatCell": {
            "range": data_range,
            "cell": {
                "userEnteredFormat": {
                    "textFormat": {
                        "fontSize": font_size,
                        "bold": bold,
                        **kwargs
                    }
                }
            },
            "fields": "userEnteredFormat.textFormat(fontSize,bold)"
        }
    }


def alignCenterCells(data_range):
    return {
        "repeatCell": {
            "range": data_range,
            "cell": {
                "userEnteredFormat": {
                    "horizontalAlignment": "CENTER",
                    "verticalAlignment": "MIDDLE"
                }
            },
            "fields": "userEnteredFormat(horizontalAlignment,verticalAlignment)"
        }
    }


def set_columns_width(data_range, width):
    d = {
        "updateDimensionProperties": {
            "range": {
                **data_range,
                "dimension": "COLUMNS",
            },
            "properties": {
                "pixelSize": width
            },
            "fields": "pixelSize"
        }
    }
    return d


def set_columns_width_auto(data_range):
    d = {
        "autoResizeDimensions": {
            "dimensions": {
                **data_range,
                "dimension": "COLUMNS",
            },
        }
    }
    return d


def setBorders(data_range, top=True, bottom=True, left=True, right=True, inner_horizontal=True, inner_vertical=True):
    single_border = {
        "style": "SOLID",  # Stile del bordo
        "width": 1,  # Larghezza del bordo in pixel
        "color": {  # Colore del bordo
            "red": 0,
            "green": 0,
            "blue": 0
        }
    }
    no_border = {}
    return {
        "updateBorders": {
            "range": data_range,
            "top": single_border if top else no_border,
            "bottom": single_border if bottom else no_border,
            "left": single_border if left else no_border,
            "right": single_border if right else no_border,
            "innerHorizontal": single_border if inner_horizontal else no_border,
            "innerVertical": single_border if inner_vertical else no_border
        }
    }


def writeCells(spreadsheet_id, data_range, content):
    if isinstance(content, str):
        content = [[content]]  # Converte una stringa in una lista di liste per una singola cella

    # Costruzione della richiesta
    return goolgle_service.sheets_service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=data_range,
        valueInputOption="USER_ENTERED",
        body={"values": content}
    ).execute()


def batch_insert_text(data_range, values):
    """
    Inserisce o aggiorna il testo in un range di celle in un Google Spreadsheet.
    Args:
    - range (str): Il range di celle dove inserire il testo (es. 'Foglio1!A1:C3').
    - values (list): Una lista di liste che contiene i valori da inserire.
    """
    return {
        'range': data_range,
        'values': values
    }


def run(spreadsheet_id, *requests):
    # Invio della richiesta batchUpdate per aggiungere il nuovo foglio
    print(list(requests))
    body = {
        'requests': list(requests)
    }
    response = goolgle_service.sheets_service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id,
                                                                         body=body).execute()
    return response


def runValues(spreadsheet_id, *datas):
    # Invio della richiesta batchUpdate per aggiungere il nuovo foglio
    body = {
        'valueInputOption': 'USER_ENTERED',
        'data': list(datas)
    }
    print("Datas:", body)
    response = goolgle_service.sheets_service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheet_id,
                                                                                  body=body).execute()
    return response


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


def num_col(num):
    col_str = ''
    while num > 0:
        resto = (num - 1) % 26
        col_str = chr(int(resto) + 65) + col_str
        num = (num - resto - 1) // 26
    return col_str


def get_sheet_id(spreadsheet_id, sheet_name):
    # Ottieni l'elenco dei fogli nello spreadsheet
    spreadsheet = goolgle_service.sheets_service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    sheets = spreadsheet.get('sheets', [])

    # Cerca l'ID del foglio corrispondente al nome
    sheet_id = None
    for sheet in sheets:
        if sheet['properties']['title'] == sheet_name:
            sheet_id = sheet['properties']['sheetId']
            break
    if sheet_id is None:
        raise ValueError(f"Sheet name '{sheet_name}' not found in the spreadsheet.")
    return sheet_id


def get_range(alpha_range):
    def column_to_index(column):
        """Converte una colonna da lettere ad indice numerico (basato su 0)."""
        index = 0
        for char in column:
            index = index * 26 + (ord(char) - ord('A') + 1)
        return index - 1

    # Separa il range in inizio e fine
    start, end = alpha_range.split(':')

    # Separa le parti alfabetiche dalle parti numeriche per inizio e fine
    start_column, start_row = ''.join(filter(str.isalpha, start)), ''.join(filter(str.isdigit, start))
    end_column, end_row = ''.join(filter(str.isalpha, end)), ''.join(filter(str.isdigit, end))

    # Converte le colonne in indici numerici e le righe in indici basati su 0
    start_column_index = column_to_index(start_column)
    end_column_index = column_to_index(end_column) + 1  # +1 perché endColumnIndex è esclusivo
    start_row_index = int(start_row) - 1
    end_row_index = int(end_row)  # Non sottraiamo 1 perché endRowIndex è esclusivo
    # Utilizza la funzione alpha_to_grid_range per convertire il range alfanumerico
    return {
        "startRowIndex": start_row_index,
        "endRowIndex": end_row_index,
        "startColumnIndex": start_column_index,
        "endColumnIndex": end_column_index,
    }


def get_data_range(sheet_id, startRowIndex=None, endRowIndex=None, startColumnIndex=None, endColumnIndex=None,
                   **kwargs):
    return {
        "sheetId": sheet_id,
        "startRowIndex": startRowIndex,
        "endRowIndex": endRowIndex,
        "startColumnIndex": startColumnIndex,
        "endColumnIndex": endColumnIndex,
        **kwargs
    }


def alpha_to_grid_range(spreadsheet_id, full_range):
    # Estrai il nome del foglio e il range alfanumerico
    sheet_name, alpha_range = full_range.split('!')

    sheet_id = get_sheet_id(spreadsheet_id, sheet_name)

    grid_range = get_range(alpha_range)

    return get_data_range(sheet_id, **grid_range)
