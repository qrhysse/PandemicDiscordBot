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

#Change location in dataframe to 'discard,' remove card from deck list and add to discard list
    def discard_top(self, card_input):
        card_name = self.find_best_match(card_input)
        
        if self.cards.at[card_name, 'forsaken'] == True:
            print(card_input + ' is forsaken. Move ' + card_input + 
                  ' to the \"Game End\" area and infect a new city.')
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
            print(card_input + ' was discarded.\n')
            if re.search('Hollow Men', card_name, re.IGNORECASE):
                print('Discard another card.\n')
 
#Use regex to find matching card that could be on top of deck. 
#If multiple choices exist, choses first option.
    def find_best_match(self, card_name):
        match_list = []
        pattern = re.escape(card_name) + '[0-9]+'
        for card in self.deck_list[0]:
            match = re.search(pattern, card)
            if match: 
                try: 
                    match_list.append(card)
                    return match_list[0] 
                except: print('That can\'t be on top!')
        
        
#Move cards from discard to deck. Add those cards to possible cards in deck list 
#and remove from discard list
    def epidemic(self):
        global infection_tracker
        for card in self.discard_list:
            self.cards.at[card, 'location'] = 'Deck'
            self.deck_list.insert(0, self.discard_list)
        self.discard_list = []
        
        #Move infection tracker up one space
        infection_tracker += 1



#Process for starting a new game
def start_game(card_df):
    #Move discard pile to deck
    card_df.replace('Discard', 'Deck', inplace=True)
    print('All discarded cards moved to the deck.')
    
    #Reset infection tracker at start of game
    global infection_tracker
    infection_tracker = 0
 


