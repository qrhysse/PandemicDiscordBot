import Pandemic
import pandas as pd


#Initializing a sample infection deck. Eventually to be replaced by a spreadsheet
cards = [\
  ['New York', False, 'Deck', None, 'Infection'], \
  ['Jacksonville', False, 'Package 6', None, 'Infection'], \
  ['New York', False, 'Deck', None, 'Infection'], \
  ['Cairo', True, 'Discard', None, 'Infection'], \
  ['Osaka', False, 'Deck', None, 'Infection'], \
  ['New York', False, 'Deck', None, 'Infection'], \
  ['New York', False, 'Deck', None, 'Infection'], \
  ['New York', True, 'Deck', None, 'Infection'], \
  ['New York', False, 'Package 6', None, 'Infection'], \
  ['London', False, 'Deck', 'Well Stocked', 'Infection'], \
  ['Hollow Men', False, 'Deck', None, 'Infection']]
    


infection_cards = pd.DataFrame(cards, columns = ['city', 'forsaken', 'location', 'stickers', 'type'])

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
#Test forsaken cities
infection_deck.discard_top('Cairo')
print('\n Infection Cards DataFrame \n')
print(infection_cards)
print('\n Possible Deck List \n')
print(infection_deck.deck_list)
print('\n Current Discard List \n')
print(infection_deck.discard_list)

print('\n    Epidemic Test')
#Test of epidemic funtion
print(Pandemic.infection_tracker)
print(Pandemic.infection_rate[Pandemic.infection_tracker])
infection_deck.epidemic()
print('\n Infection Cards DataFrame \n')
print(infection_cards)
print('\n Possible Deck List \n')
print(infection_deck.deck_list)
print('\n Current Discard List \n')
print(infection_deck.discard_list)
print(Pandemic.infection_tracker)
print(Pandemic.infection_rate[Pandemic.infection_tracker])

print('\n Wearing Off Test\n')
infection_deck.wear_off('Jacksonville')
print(infection_cards)
print(infection_deck.package_list)
print(infection_deck.discard_list)

print('\n Inoculate Test \n')
infection_deck.inoculate('Jacksonville')
print(infection_cards)
print('\n Current Package 6 Contents \n')
print(infection_deck.package_list)

#Test discarding a card that can't be on top of the deck
# try: infection_deck.discard_top('Jacksonville')
# except: print('That can\'t be on top!')
print('\n Possible Deck List \n')
print(infection_deck.deck_list)
print('\n Possible Cards on top X')
print(infection_deck.top_x_cards(8))

print('\nCards that will be drawn in next X cards')
print(infection_deck.create_probablility_dict(4))

infection_deck.predict_next_infect_cities()
