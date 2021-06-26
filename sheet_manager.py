from __future__ import print_function
import gspread
import pandas as pd
import re

SERVICE_ACCOUNT_FILE = 'keys.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
              'https://www.googleapis.com/auth/drive']

gc = gspread.service_account(SERVICE_ACCOUNT_FILE, SCOPES)
sh = gc.open("Pandemic Legacy Sheet")
worksheet = sh.get_worksheet(1)

def setup_dataframe():
    

    cards_df = pd.DataFrame(worksheet.get_all_records())
    cards_df.columns = cards_df.columns.str.lower().str.replace(' ', '_')
    cards_df.dropna(how='all', axis=1, inplace=True)
    cards_df.fillna('', inplace=True)
    cards_df['forsaken'].replace(
                     to_replace={'TRUE': True, 'FALSE': False},inplace=True)
    cards_df['sticker'] = cards_df.sticker.str.lower()
    n_mask = lambda x: '{} ({})'.format(x.card_name.lower(), x.sticker)
    cards_df['card_name'] = cards_df.apply(n_mask, axis=1)
    cards_df['card_name'].replace(
                      to_replace=" \(\)$", value='', inplace=True, regex=True)
    cards_df.sort_values(['card_name', 'location'], inplace=True, ignore_index=True)
    u_mask = lambda x: '{} {}'.format(x.card_name, x.name)
    cards_df['unique_name'] = cards_df.apply(u_mask, axis=1)
    cards_df.set_index('unique_name', inplace=True, drop=True)

    return(cards_df)

def update_spreadsheet(cards_df):
    clean_df = cards_df.copy()
    clean_df['card_name'].replace(
                      to_replace="( \(.*\))?", value='', inplace=True, regex=True)
    clean_df['card_name'] = clean_df.card_name.str.title()
    clean_df.columns = clean_df.columns.str.title().str.replace('_', ' ')
    worksheet.update([clean_df.columns.values.tolist()] + clean_df.values.tolist())
#creds = service_account.Credentials.from_service_account_file(
        #SERVICE_ACCOUNT_FILE, scopes=SCOPES)
#client = gspread.authorize(creds)

#spreadsheet = client.open('133EKlMVdgp8e-aEEiBsV4NPdttHHDfk0JKvQfNXASUw')
