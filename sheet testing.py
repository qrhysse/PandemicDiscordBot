
import pandas as pd
import sheet as sh
import re
import pandemic

SPREADSHEET_ID = '133EKlMVdgp8e-aEEiBsV4NPdttHHDfk0JKvQfNXASUw'
spreadsheet = sh.sheet_to_df(SPREADSHEET_ID)

infection_cards = pd.DataFrame(spreadsheet[0], columns = spreadsheet[1])
infection_cards['card_name'] = infection_cards['card_name'].str.lower()
infection_cards.sort_values(['card_name', 'location'],
                             inplace=True, ignore_index=True)
infection_cards['unique_name'] = infection_cards.card_name + \
                                 infection_cards.index.map(str)
infection_cards.set_index('unique_name', inplace=True, drop=False)
infection_cards['forsaken'] = infection_cards.apply(lambda x: \
                                True if x.forsaken == 'TRUE' else False, axis=1)
infection_deck = pandemic.Deck(infection_cards, 'Infection')

while True:
    command = input("Command: ").lower()
    if re.search("start game", command):
        pandemic.start_game(infection_cards)
        print('Infection Deck\n')
        print(infection_deck.cards)
    elif re.search('flip', command):
        card_name = command[5:]
        try: infection_deck.discard_top(card_name)
        except: print('That card isn\t there!')
    elif re.search('inoculate', command):
        card_name = command[10:]
        try: infection_deck.inoculate(card_name)
        except: print('That card isn\t there!')
    elif re.search('wear off', command):
        card_name = command[9:]
        try: infection_deck.wear_off(card_name)
        except: print('That card isn\t there!')
    elif re.search('epidemic', command):
        infection_deck.epidemic()
    elif re.search('top(( )| \d? )cards?', command):
        temp_list = re.findall(r'\d+', command) + ['1']
        x = int(temp_list[0])
        infection_deck.top_x_cards(x)
    elif re.search('next(( )| \d? )cards? odds', command):
        temp_list = re.findall(r'\d+', command) + ['1']
        x = int(temp_list[0])
        infection_deck.create_probablility_dict(x)
