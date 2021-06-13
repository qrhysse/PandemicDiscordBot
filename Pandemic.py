import pandas as pd

#The number of cards that are flipped during infect cities step
infection_tracker = 2

#Initializing a sample infection deck. Eventually to be replaced by a spreadsheet
cards = [\
  ['New York', None, 'Deck'], \
  ['Jacksonville', None, 'Deck'], \
  ['New York', None, 'Deck'], \
  ['Cairo', None, 'Discard'], \
  ['Osaka', None, 'Deck'], \
  ['New York', None, 'Deck'], \
  ['New York', None, 'Deck'], \
  ['New York', None, 'Deck'], \
  ['New York', None, 'Package 6']]
    
infection_cards = pd.DataFrame(cards, columns = ['city', 'range', 'location'])

#Sort by city name and create a unique ID for each infection card: city name + index
infection_cards.sort_values(['city', 'location'], inplace=True, ignore_index=True)
infection_cards['unique_name'] = infection_cards.city + infection_cards.index.map(str)
infection_cards.set_index('unique_name', drop=False, inplace=True)

#print(infection_cards)


#Process for starting a new game
def start_game(card_df):
    #Move discard pile to deck
    card_df.replace('Discard', 'Deck', inplace=True)

# cards_in_deck = infection_cards[infection_cards.location == 'Deck']
# infection_deck = [[card for card in cards_in_deck['unique_name']] for i in range(len(cards_in_deck))]
# print(infection_deck)

# def to_discard(card_df, card_unique_name):
#     card_df[card_unique_name].location = 'Discard'
    
    
start_game(infection_cards)

class Deck:
    def __init__(self, card_df, card_type):
        self.type = card_type
        self.cards = card_df
        self.in_deck = card_df[card_df.location == 'Deck']
        self.deck_size = len(self.in_deck)
        self.deck_list = [[card for card in self.in_deck.unique_name] \
                          for x in range(self.deck_size)]
        self.discard_list = [card for card in card_df[card_df.location == 'Discard'].unique_name]
         
    def discard_top(self, card_name):
        self.cards.at[card_name, 'location'] = 'Discard'
        del self.deck_list[0]
        for slot in self.deck_list:
            slot.remove(card_name)
        self.discard_list.insert(0, card_name)
        
#Move cards from discard to deck. Add those cards to possible cards in deck list 
#and remove from discard list
    def epidemic(self):
        for card in self.discard_list:
            print(card)
            self.cards.at[card, 'location'] = 'Deck'
            self.deck_list.insert(0, self.discard_list)
        self.discard_list = []
        

infection_deck = Deck(infection_cards, 'infection')
print(infection_cards)
print(infection_deck.discard_list)
infection_deck.discard_top('New York2')
infection_deck.discard_top('Osaka8')

print(infection_cards)
print(infection_deck.deck_list)
print(infection_deck.discard_list)

infection_deck.epidemic()
print(infection_cards)
print(infection_deck.deck_list)
print(infection_deck.discard_list)