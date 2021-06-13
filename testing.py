import Pandemic
import pandas as pd


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
  ['London', False, 'Deck', 'Well Stocked'], \
  ['Hollow Men', False, 'Deck', None]
      ]
    
infection_cards = pd.DataFrame(cards, columns = ['city', 'forsaken', 'location', 'stickers'])

#Sort by city name and create a unique ID for each infection card: city name + index
infection_cards.sort_values(['city', 'location'], inplace=True, ignore_index=True)
infection_cards['unique_name'] = infection_cards.city + infection_cards.index.map(str)
infection_cards.set_index('unique_name', drop=False, inplace=True)

Pandemic.start_game(infection_cards)

#Test game scenario
print('\n    Start Test Game')
infection_deck = Pandemic.Deck(infection_cards, 'Infection')

print('\n Infection Cards DataFrame \n')
print(infection_cards)
print('\n Possible Deck List \n')
print(infection_deck.deck_list)
print('\n Current Discard List \n')
print(infection_deck.discard_list)

#Discard two cards to mimic infect cities step at end of turn
print('\n    Infect one card and Hollow Men arrive in another')
infection_deck.discard_top('New York')
infection_deck.discard_top('Hollow Men')
infection_deck.discard_top('Osaka')
#Print the card Dataframe, deck list, and discard list to verify discard functionality
print('\n Infection Cards DataFrame \n')
print(infection_cards)
print('\n Possible Deck List \n')
print(infection_deck.deck_list)
print('\n Current Discard List \n')
print(infection_deck.discard_list)

print('\n    Infect a forsaken city')

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
