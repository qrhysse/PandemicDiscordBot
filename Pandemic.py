import re

#The number of cards that are flipped during infect cities step
infection_rate = [2, 2, 2, 3, 3, 4, 4, 5]
infection_tracker = 0

class Deck:
    def __init__(self, card_df, card_type):
        self.type = card_type
        self.cards = card_df
        self.in_deck = card_df[card_df.location == 'Deck']
        self.deck_size = len(self.in_deck)
        self.deck_list = [[card for card in self.in_deck.unique_name] \
                          for x in range(self.deck_size)]
        self.discard_list = [card for card in card_df[card_df.location == 'Discard'].unique_name]
        self.package_list = [card for card in card_df[card_df.location == 'Package 6'].unique_name]
        
        
        
    #Use regex to find matching card that could be on top of deck. 
    #If multiple choices exist, choses first option.
    def find_best_match(self, card_input, card_list):
        pattern = re.escape(card_input) + '[0-9]+'
        for card in card_list:
            match = re.search(pattern, card)
            if match: return card
            
    def remove_from_card_list(self, card_input, card_list):
        card_list.remove(card_input)
        
    def move_to_discard(self, card_input):
        self.cards.at[card_input, 'location'] = 'Discard'
        self.discard_list.insert(0, card_input)
    
    def move_to_package(self, card_input):
        self.cards.at[card_input, 'location'] = 'Package 6'
        self.package_list.insert(0, card_input)

    #Change location in dataframe to 'discard,' remove card from deck list and add to discard list
    def discard_top(self, card_input):
        card_name = self.find_best_match(card_input, self.deck_list[0])
        del self.deck_list[0]
        #Reminder to infect another city if this city is forsake. Moves card to game end area
        if self.cards.at[card_name, 'forsaken'] == True:
            for slot in self.deck_list:
                self.remove_from_card_list(card_name, slot)
            self.cards.at[card_name, 'location'] = 'Game End'
            print(card_input + ' is forsaken. Move ' + card_input + 
                  ' to the \"Game End\" area and infect a new city.')
        else:
            self.move_to_discard(card_name)
            for slot in self.deck_list:
                self.remove_from_card_list(card_name, slot)
            print(card_input + ' was discarded.\n')
            #Reminder to discard another card for Hollow Men effect
            if re.search('Hollow Men', card_name, re.IGNORECASE):
                print('Discard another card.\n')
 
    #Move card from Package 6 to discard pile
    def wear_off(self, card_input):
        card_name = self.find_best_match(card_input, self.package_list)
        self.move_to_discard(card_name)
        self.remove_from_card_list(card_name, self.package_list)
    
    #Move card from discard pile to package 6
    def inoculate(self, card_input):
        card_name = self.find_best_match(card_input, self.discard_list)
        self.move_to_package(card_name)
        self.remove_from_card_list(card_name, self.discard_list)
        
    #Move cards from discard to deck. Add those cards to possible cards in deck list 
    #and remove from discard list. 
    def epidemic(self):
        #Increase infection tracker by 1
        global infection_tracker
        infection_tracker += 1
        
        for card in self.discard_list:
            self.cards.at[card, 'location'] = 'Deck'
            self.deck_list.insert(0, self.discard_list)
        self.discard_list = []
        
        
        
    
    
        
    
    
    
            



#Process for starting a new game
def start_game(card_df):
    #Move discard pile to deck
    card_df.replace('Discard', 'Deck', inplace=True)
    print('All discarded cards moved to the deck.')
    
    #Reset infection tracker at start of game
    global infection_tracker
    infection_tracker = 0
 


