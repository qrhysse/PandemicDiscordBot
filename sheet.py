from __future__ import print_function
from googleapiclient.discovery import build
from google.oauth2 import service_account


SERVICE_ACCOUNT_FILE = 'keys.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)


service = build('sheets', 'v4', credentials=creds)

def sheet_to_df(SHEET_ID):
    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SHEET_ID,
                                range='cardscopy!A1:K99').execute()
    values = result.get('values', [])

    cols = [x.lower().replace(' ', '_') for x in values[0]]
    data = values[1:]

    return data, cols
