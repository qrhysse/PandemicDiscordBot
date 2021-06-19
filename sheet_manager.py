
import pandas as pd
#import sheet as sh
import re
#import pandemic

#SPREADSHEET_ID = '133EKlMVdgp8e-aEEiBsV4NPdttHHDfk0JKvQfNXASUw'
#spreadsheet = sh.sheet_to_df(SPREADSHEET_ID)
#cards_df = pd.DataFrame(spreadsheet[0], columns = spreadsheet[1])

def setup_dataframe():
    sheet_id = '133EKlMVdgp8e-aEEiBsV4NPdttHHDfk0JKvQfNXASUw'
    sheet_name = 'CardsCopy'
    cards_df = pd.read_csv(
        'https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}'
        .format(sheet_id, sheet_name))

    cards_df.columns = cards_df.columns.str.lower().str.replace(' ', '_')
    cards_df.dropna(how='all', axis=1, inplace=True)
    cards_df.fillna('', inplace=True)
    cards_df['forsaken'].replace(
                     to_replace={'TRUE': True, 'FALSE': False},inplace=True)
    cards_df['sticker'] = cards_df.sticker.str.lower()
    n_mask = lambda x: '{} {}'.format(x.card_name.lower(), x.sticker)
    cards_df['card_name'] = cards_df.apply(n_mask, axis=1)
    cards_df['card_name'].replace(
                      to_replace="\s+$", value='', inplace=True, regex=True)
    cards_df.sort_values(['card_name', 'location'], inplace=True, ignore_index=True)
    u_mask = lambda x: '{} {}'.format(x.card_name, x.name)
    cards_df['unique_name'] = cards_df.apply(u_mask, axis=1)
    cards_df.set_index('unique_name', inplace=True, drop=True)

    return(cards_df)
