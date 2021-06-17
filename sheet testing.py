# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 15:12:45 2021

@author: Chris
"""
import pandas as pd
import Pandemic

sheet_url = 'https://docs.google.com/spreadsheets/d/133EKlMVdgp8e-aEEiBsV4NPdttHHDfk0JKvQfNXASUw/edit#gid=0'
csv_url = 'https://docs.google.com/spreadsheets/d/133EKlMVdgp8e-aEEiBsV4NPdttHHDfk0JKvQfNXASUw/export?format=csv'

infection_cards = pd.read_csv('pandemic sheet.csv')
infection_cards.columns = ['city', 'location', 'color', 'sticker', 'forsaken', 'type']
                              
                              
    
#['city', 'location', 'color', 'sticker', 'forsaken', 'type']
    
infection_cards.sort_values(['city', 'location'], inplace=True, ignore_index=True)
infection_cards['unique_name'] = infection_cards.city + infection_cards.index.map(str)
#infection_cards.set_index('unique_name', drop=False, inplace=True)

Pandemic.start_game(infection_cards)
infection_deck = Pandemic.Deck(infection_cards, 'Infection')

print(infection_deck.cards)


# print('\n Infection Cards DataFrame \n')
# print(infection_cards.head())
# print('\n Possible Deck List \n')
# print(infection_deck.deck_list)
# print('\n Current Discard List \n')
# print(infection_deck.discard_list)