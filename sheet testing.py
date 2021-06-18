# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 15:12:45 2021

@author: Chris
"""
import pandas as pd
import sheet as sh
import pandemic

SPREADSHEET_ID = '133EKlMVdgp8e-aEEiBsV4NPdttHHDfk0JKvQfNXASUw'
spreadsheet = sh.sheet_to_df(SPREADSHEET_ID)
infection_cards = pd.DataFrame(spreadsheet[0], columns = spreadsheet[1])

infection_cards.sort_values(['card_name', 'location'], inplace=True, ignore_index=True)
infection_cards['unique_name'] = infection_cards.card_name + infection_cards.index.map(str)
#infection_cards.set_index('unique_name', drop=False, inplace=True)

pandemic.start_game(infection_cards)
infection_deck = pandemic.Deck(infection_cards, 'Infection')

print(infection_deck.cards)


# print('\n Infection Cards DataFrame \n')
# print(infection_cards.head())
# print('\n Possible Deck List \n')
# print(infection_deck.deck_list)
# print('\n Current Discard List \n')
# print(infection_deck.discard_list)
