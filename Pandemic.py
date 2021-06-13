import pandas as pd
import re

#The number of cards that are flipped during infect cities step
infection_tracker = 2

#Initializing a sample infection deck. Eventually to be replaced by a spreadsheet
cards = [\
  ['New York', False, 'Deck', None], \
  ['Jacksonville', False, 'Deck', None], \
  ['New York', False, 'Deck', None], \
  ['Cairo', True, 'Discard', None], \
  ['Osaka', False, 'Deck', None], \
  ['New York', False, 'Deck', None], \
  ['New York', False, 'Deck', None], \
  ['New York', True, 'Deck', None], \
  ['New York', False, 'Package 6', None], \
  ['London', False, 'Deck', 'Well Stocked'] \
      ]
    
infection_cards = pd.DataFrame(cards, columns = ['city', 'forsaken', 'location', 'stickers'])

#Sort by city name and create a unique ID for each infection card: city name + index
infection_cards.sort_values(['city', 'location'], inplace=True, ignore_index=True)
infection_cards['unique_name'] = infection_cards.city + infection_cards.index.map(str)
infection_cards.set_index('unique_name', drop=False, inplace=True)


class Deck:
    def __init__(self, card_df, card_type):
        self.type = card_type
        self.cards = card_df
        self.in_deck = card_df[card_df.location == 'Deck']
        self.deck_size = len(self.in_deck)
        self.deck_list = [[card for card in self.in_deck.unique_name] \
                          for x in range(self.deck_size)]
        self.discard_list = [card for card in card_df[card_df.location == 'Discard'].unique_name]

#Change location in dataframe to 'discard,' remove card from deck list and add to discard list
    def discard_top(self, card_input):
        card_name = self.find_best_match(card_input)
        if self.cards.at[card_name, 'forsaken'] == True:
            print('Move the card to the \"Game End\" area and infect a new city.')
            self.cards.at[card_name, 'location'] = 'Game End'
            del self.deck_list[0]
            for slot in self.deck_list:
                slot.remove(card_name)
        else:
            self.cards.at[card_name, 'location'] = 'Discard'
            del self.deck_list[0]
            for slot in self.deck_list:
                slot.remove(card_name)
            self.discard_list.insert(0, card_name)
 
#Use regex to find matching card that could be on top of deck. 
#If multiple choices exist, choses first option.
    def find_best_match(self, card_name):
        match_list = []
        pattern = re.escape(card_name) + '[0-9]+'
        for card in self.deck_list[0]:
            match = re.search(pattern, card)
            if match: 
                match_list.append(card)
        try: return match_list[0]
        except: 
            print('That can\'t be on top!')
        
#Move cards from discard to deck. Add those cards to possible cards in deck list 
#and remove from discard list
    def epidemic(self):
        for card in self.discard_list:
            self.cards.at[card, 'location'] = 'Deck'
            self.deck_list.insert(0, self.discard_list)
        self.discard_list = []



#Process for starting a new game
def start_game(card_df):
    #Move discard pile to deck
    card_df.replace('Discard', 'Deck', inplace=True)
 
start_game(infection_cards)

#Test game scenario
print('\n    Start Test Game')
infection_deck = Deck(infection_cards, 'infection')
print('\n Infection Cards DataFrame \n')
print(infection_cards)
print('\n Possible Deck List \n')
print(infection_deck.deck_list)
print('\n Current Discard List \n')
print(infection_deck.discard_list)

#Discard two cards to mimic infect cities step at end of turn
print('\n    Infect New York and Osaka')
infection_deck.discard_top('New York')
infection_deck.discard_top('Osaka')
#Print the card Dataframe, deck list, and discard list to verify discard functionality
print('\n Infection Cards DataFrame \n')
print(infection_cards)
print('\n Possible Deck List \n')
print(infection_deck.deck_list)
print('\n Current Discard List \n')
print(infection_deck.discard_list)

print('\n    Infect a forsaken city')
#Test discarding 0 population city
infection_deck.discard_top('Cairo')
print('\n Infection Cards DataFrame \n')
print(infection_cards)
print('\n Possible Deck List \n')
print(infection_deck.deck_list)
print('\n Current Discard List \n')
print(infection_deck.discard_list)

print('\n    Epidemic Test')
#Test of epidemic funtion
infection_deck.epidemic()
print('\n Infection Cards DataFrame \n')
print(infection_cards)
print('\n Possible Deck List \n')
print(infection_deck.deck_list)
print('\n Current Discard List \n')
print(infection_deck.discard_list)

#Test discarding 0 population city
#infection_deck.discard_top('Cairo')