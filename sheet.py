from __future__ import print_function
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account


SERVICE_ACCOUNT_FILE = 'keys.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)


# The ID and range of a sample spreadsheet.


service = build('sheets', 'v4', credentials=creds)

def sheet_to_df(SHEET_ID):
    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SHEET_ID,
                                range='cards!A1:K99').execute()
    values = result.get('values', [])

    cols = [x.lower().replace(' ', '_') for x in values[0]]
    data = values[1:]

    return data, cols



# if not values:
#         print('No data found.')
# else:
#     print('Name, Major:')
#     for row in values:
#         # Print columns A and E, which correspond to indices 0 and 4.
#         print('%s, %s' % (row[0], row[4]))
