
import pandas as pd
#import sheet as sh
import re
import pandemic

#SPREADSHEET_ID = '133EKlMVdgp8e-aEEiBsV4NPdttHHDfk0JKvQfNXASUw'
#spreadsheet = sh.sheet_to_df(SPREADSHEET_ID)
#cards_df = pd.DataFrame(spreadsheet[0], columns = spreadsheet[1])

sheet_id = '133EKlMVdgp8e-aEEiBsV4NPdttHHDfk0JKvQfNXASUw'
sheet_name = 'CardsCopy'
cards_df = pd.read_csv(
        'https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}'
        .format(sheet_id, sheet_name))

cards_df.columns = cards_df.columns.str.lower().str.replace(' ', '_')
cards_df.dropna(how='all', axis=1, inplace=True)
cards_df['card_name'] = cards_df['card_name'].str.lower()
cards_df['forsaken'] = cards_df.apply(lambda x:
                             True if x.forsaken == 'TRUE' else False, axis=1)
cards_df['sticker'] = cards_df.apply(lambda x:
                             None if x.sticker == 'None' else x.sticker, axis=1)
cards_df.sort_values(['card_name', 'location'],
                             inplace=True, ignore_index=True)
cards_df['unique_name'] = cards_df.card_name + cards_df.index.map(str)
cards_df.set_index('unique_name', inplace=True, drop=False)

infection_deck = pandemic.Deck(cards_df, 'Infection')

while True:
    command = input("Command: ").lower()
    if re.search("start game", command):
        pandemic.start_game(cards_df)
        print('Infection Deck\n')
        print(infection_deck.cards)
    elif re.search('flip', command):
        card_name = command[5:]
        try: infection_deck.discard_top(card_name)
        except: print('That card isn\t there!')
        print(infection_deck.discard_list)
    elif re.search('inoculate', command):
        card_name = command[10:]
        try: infection_deck.inoculate(card_name)
        except: print('That card isn\t there!')
        print(infection_deck.discard_list)
        print(infection_deck.package_list)
    elif re.search('wear off', command):
        card_name = command[9:]
        try: infection_deck.wear_off(card_name)
        except: print('That card isn\t there!')
        print(infection_deck.discard_list)
        print(infection_deck.package_list)
    elif re.search('epidemic', command):
        infection_deck.epidemic()
        print(infection_deck.discard_list)
    elif re.search('top(( )| \d? )cards?', command):
        temp_list = re.findall(r'\d+', command) + ['1']
        x = int(temp_list[0])
        infection_deck.top_x_cards(x)
    elif re.search('next(( )| \d? )cards? odds', command):
        temp_list = re.findall(r'\d+', command) + ['1']
        x = int(temp_list[0])
        print(infection_deck.create_probablility_dict(x))
    elif re.search('predict infect cities', command):
        infection_deck.predict_next_infect_cities()
    elif re.search('show cards', command):
        print infection_deck.cards
