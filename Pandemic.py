import re
from collections import Counter

#decimal.getcontext().rounding = decimal.ROUND_HALF_UP
#The number of cards that are flipped during infect cities step
inf_rate = [2, 2, 2, 3, 3, 4, 4, 5]
inf_tracker = 0

class Deck:
    def __init__(self, card_df, card_type):
        self.type = card_type
        self.cards = card_df[card_df.card_type == self.type]
        self.in_deck = card_df[card_df.location == 'Deck']
        self.deck_size = len(self.in_deck)
        self.deck_list = [[card for card in self.in_deck.unique_name] \
                          for x in range(self.deck_size)]
        self.discard_list = [card for card in \
                             card_df[card_df.location == 'Discard'].unique_name]
        self.package_list = [card for card in \
                             card_df[card_df.location == 'Package 6'].unique_name]



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
        del self.deck_list[0]

    def discard_bot(self, card_input):
        card_name = self.find_best_match(card_input, self.deck_list[-1])
        #Reminder to infect another city if this city is forsaken. Moves card to game end area
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
        del self.deck_list[-1]


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
        print('1-Increase')
        global inf_tracker
        inf_tracker += 1
        print('Infection Tracker is at {}'.format(inf_rate[inf_tracker]))
        print('2-Infect\n Flip the bottom card')
        bot_card = input('What was the bottom card?').lower()
        self.discard_bot(bot_card)
        print('''3-Intensify\n
              Shuffle the discard pile and place on top of the deck''')
        for card in self.discard_list:
            self.cards.at[card, 'location'] = 'Deck'
            self.deck_list.insert(0, self.discard_list)
        self.discard_list = []

    #Returns lists of possible cards in each slot
    def top_x_cards(self, x):
        answer = ''
        for i in range(x):
            answer += ('\nCard {0} possibilities: {1}\n'
                        .format(i+1, self.deck_list[i]))
        print(answer)

    #Retuirns a dictionary of each card and how many will be drawn in the top x cards
    def create_probablility_dict(self, top_cards):
        deck_slot = [self.deck_list[i] for i in range(top_cards)]

        no_unique_slots = []
        for slot in deck_slot:
            no_unique_list = []
            for card in slot:
                card_name = ''.join(i for i in card if not i.isdigit())
                no_unique_list.append(card_name)
            no_unique_slots.append(no_unique_list)

        list_of_dicts = []
        for slot in no_unique_slots:
            counted_dict = {card:slot.count(card) for card in slot}
            list_of_dicts.append(counted_dict)

        end_dict = {}
        for slot in list_of_dicts:
            total = sum(slot.values())
            for k, v in slot.items():
                odds = (float(v) / total)
                slot[k] = round(odds, 10)
            end_dict = dict(Counter(end_dict) + Counter(slot))
        for k, v in end_dict.items():
            end_dict[k] = round(v, 2)
        sorted_odds = {k: v for k, v in \
                sorted(end_dict.items(), key=lambda item: item[1], reverse=True)}
        print(sorted_odds)


    def predict_next_infect_cities(self):
        prediction_dict = self.create_probablility_dict(infection_rate[infection_tracker])
        print('In the next infect cities step, you will probably hit: {}'.format(prediction_dict))



#Process for starting a new game
def start_game(card_df):
    #Move discard pile to deck
    card_df.replace('Discard', 'Deck', inplace=True)
    print('All discarded cards moved to the deck.')
    #Reset infection tracker at start of game
    global infection_tracker
    infection_tracker = 0
