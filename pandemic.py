import re
from collections import Counter

#decimal.getcontext().rounding = decimal.ROUND_HALF_UP
#The number of cards that are flipped during infect cities step
inf_rate = [2, 2, 2, 3, 3, 4, 4, 5]
inf_tracker = 0

class Deck:
    def __init__(self, card_df, card_type):
        self.reset(card_df, card_type)


    def reset(self, card_df, card_type):
        self.type = card_type
        self.cards = card_df.loc[card_df.card_type == self.type]
        self.in_deck = card_df[card_df.location == 'Deck']
        self.deck_size = len(self.in_deck)
        self.deck_list = [[card for card in self.in_deck.index]
                          for x in range(self.deck_size)]
        self.discard_list = [card for card in
                           card_df[card_df.location == 'Discard'].index]
        self.package_list = [card for card in
                           card_df[card_df.location == 'Package 6'].index]
    #Use regex to find matching card that could be on top of deck.
    #If multiple choices exist, choses first option.
    def find_best_match(self, card_input, card_list):
        pattern = re.escape(card_input) + ' [0-9]+$'
        for card in card_list:
            match = re.fullmatch(pattern, card)
            if match:
                print(card+' was a match')
                return card

    def move_to_discard(self, card_input):
        self.cards.at[card_input, 'location'] = 'Discard'
        print(card_input+' was moved to discard')
        self.discard_list.insert(0, card_input)
        self.discard_list.sort()

    def move_to_package(self, card_input):
        self.cards.at[card_input, 'location'] = 'Package 6'
        print(card_input+' was moved to Package 6')
        self.package_list.insert(0, card_input)
        self.package_list.sort()

    #Change location in dataframe to 'discard'
    #remove card from deck list and add to discard list
    def discard_top(self, card_input):
        card_name = self.find_best_match(card_input, self.deck_list[0])
        #Reminder to infect another city if this city is forsake.
        #Moves card to game end area
        answer = ''
        if self.cards.at[card_name, 'forsaken'] == True:
            for slot in self.deck_list: slot.remove(card_name)
            self.cards.at[card_name, 'location'] = 'Game End'
            answer = '{0} is forsaken.\n \
                      Move {0} to the \"Game End\" area and infect a new city.'\
                      .format(card_input.title())
        else:
            self.move_to_discard(card_name)
            for slot in self.deck_list: slot.remove(card_name)
            answer = card_input.title() + ' was discarded.\n'
            #Reminder to discard another card for Hollow Men effect
            if re.search('HMG', card_name, re.IGNORECASE):
                answer += 'Discard another card.\n'
        del self.deck_list[0]
        print(answer)
        return(answer)

#Discard bottom card. Currently not in use
    def discard_bot(self, card_input):
        card_name = self.find_best_match(card_input, self.deck_list[-1])

        self.move_to_discard(card_name)
        for slot in self.deck_list: slot.remove(card_name)
        #Reminder to discard another card for Hollow Men effect
        if re.search('HMG', card_name, re.IGNORECASE):
            print('Discard another card.\n')
        #Reminder to infect another city if this city is forsaken.
        #Moves card to game end area
        elif self.cards.at[card_name, 'forsaken'] == True:
            self.cards.at[card_name, 'location'] = 'Game End'
            self.discard_list.remove(card_name)
            print(card_input + ' is forsaken. Move ' + card_input +
                      ' to the \"Game End\" area and infect a new city.')
        else: print(card_input + ' was discarded.\n')
        del self.deck_list[-1]


    #Move card from Package 6 to discard pile
    def wear_off(self, card_input):
        card_name = self.find_best_match(card_input, self.package_list)
        self.move_to_discard(card_name)
        self.package_list.remove(card_name)
        self.package_list.sort()

    #Move card from discard pile to package 6
    def inoculate(self, card_input):
        card_name = self.find_best_match(card_input, self.discard_list)
        self.move_to_package(card_name)
        self.discard_list.remove(card_name)
        self.discard_list.sort()

    def destroy_card(self, card_input):
        card_name = self.find_best_match(card_input, self.discard_list)
        self.cards.at[card_input, 'location'] = 'Trash'
        self.discard_list.remove(card_name)
        self.discard_list.sort()

    #Move cards from discard to deck. Add those cards to possible cards in deck
    #and remove from discard list.
    def epidemic(self, card_input):
        self.wear_off(card_input)
        for card in self.discard_list:
            self.cards.at[card, 'location'] = 'Deck'
            self.deck_list.insert(0, self.discard_list)
        self.discard_list = []

    #Returns lists of possible cards in each slot
    def top_x_cards(self, x):
        answer = ''
        for i in range(x):
            slot = [re.sub(' [0-9]+$', '', x) for x in self.deck_list[i]]
            c = {key: value for key, value in Counter(slot).items()}
            sort_c = sorted(c.items(), key=lambda x:x[1], reverse=True)
            answer += ('\nCard {0} possibilities: \n{1}'
                        .format(i+1, sort_c))
        return answer

    #Retuirns a dictionary of each card
    #and how many will be drawn in the top x cards
    #sorted by odds of being drawn
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
        sorted_odds = {k: v for k, v in
                sorted(end_dict.items(),
                key=lambda item: item[1],
                reverse=True)}
        return str(sorted_odds)


    def predict_next_infect_cities(self):
        prediction_dict = self.create_probablility_dict(inf_rate[inf_tracker])
        answer = 'In the next infect cities step, you will probably hit: \n{}'\
                .format(prediction_dict)
        return answer




#Process for starting a new game
def start_game(deck):

    #Move discard pile to deck
    deck.cards.replace('Discard', 'Deck', inplace=True)
    deck.cards.replace('Game End', 'Deck', inplace=True)
    hollows = deck.cards.loc[deck.cards.card_name=='hmg']
    deck.cards.apply(lambda x:
        deck.move_to_discard(x.name) if x.card_name=='hmg'
        else None, axis = 1)
    return(deck)
    #Reset infection tracker at start of game
    global infection_tracker
    infection_tracker = 0

def increase_inf_rate():
    global inf_tracker
    inf_tracker += 1
