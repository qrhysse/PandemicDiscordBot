import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import pandemic as pan
import sheet_manager as sm

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')
client = commands.Bot(command_prefix='.')

cards_df = sm.setup_dataframe()
infection_deck = pan.Deck(cards_df, 'Infection')

@client.event
async def on_ready():
    print('PandyBot is ready to save the world!')

#Start new game
@client.command(aliases = ['start'], brief='Reset the deck for a new game.')
async def start_game(ctx):
    sm.worksheet.format('I5:J6', {
                    "backgroundColor": {"red": 1.0, "green": 0.0, "blue": 0.0}})
    reset_deck = pan.start_game(infection_deck)
    update_sheet(reset_deck.cards)
    infection_deck.reset(cards_df, infection_deck.type)
    await ctx.send(f'Game started!')

#Stop editing spreadsheet
@client.command(aliases = ['stop'], brief='Change color of edit cells.')
async def stop_game(ctx):
    sm.worksheet.format('I5:J6', {
                    "backgroundColor": {"red": 1.0, "green": 1.0, "blue": 1.0}})

#Change deck to match spreadsheet
@client.command(brief='Update the deck after changing the spreadsheet')
async def update(ctx):
    global cards_df
    global infection_deck
    cards_df = sm.setup_dataframe()
    infection_deck = pan.Deck(cards_df, 'Infection')

#Check state command
@client.command(brief='Check the current state of the game')
async def state(ctx):
    await ctx.send(
       f'\nInfection Discard Pile: {len(infection_deck.discard_list)} cards\n' +
       str(infection_deck.discard_list))
    await ctx.send(
       f'Package 6 Contents: {len(infection_deck.package_list)} cards\n' +
       str(infection_deck.package_list))

#Infect city command
@client.command(aliases=['discard', 'infect', 'f'],
                brief='Discard the top of the infection deck')
async def flip(ctx, *, card):
    try:
        await ctx.send(infection_deck.discard_top(card))
        await ctx.send(
        f'Infection Discard Pile: {len(infection_deck.discard_list)} cards\n' +
        str(infection_deck.discard_list))
        update_sheet(infection_deck.cards)
    except:
        await ctx.send('I don\'t think that\'s right')

#Inoculate command
@client.command(aliases=['innoculate', 'package', 'exile', 'i'],
                brief='Move a card from Discard to Package 6')
async def inoculate(ctx, *, card):
    try:
        infection_deck.inoculate(card)
        await ctx.send(f'{card.title()} was inoculated.\n'
            f'Package 6 Contents: {len(infection_deck.package_list)} cards\n' +
            str(infection_deck.package_list))
        await ctx.send(
            f'\nInfection Discard Pile: {len(infection_deck.discard_list)} cards\n' +
            str(infection_deck.discard_list))
        update_sheet(infection_deck.cards)
    except:
        await ctx.send('I don\'t think that\'s right')

#Wear off command
@client.command(aliases=['wear', 'unoculate', 'w'],
                brief='Move a card from Package 6 to Discard')
async def wear_off(ctx, *, card):
    try:
        infection_deck.wear_off(card)
        await ctx.send(f'{card.title()}\'s inoculation wore off.\n'
            f'Package 6 Contents: {len(infection_deck.package_list)} cards\n' +
            str(infection_deck.package_list))
        await ctx.send(
            f'\nInfection Discard Pile: {len(infection_deck.discard_list)} cards\n' +
            str(infection_deck.discard_list))
        update_sheet(infection_deck.cards())
    except:
        await ctx.send('I don\'t think that\'s right')

#Destroy card command
@client.command(aliases = ['destroy', 'trash', 'd'],
                brief='Move a card from Discard to Trash')
async def destroy_card(ctx, *, card):
    try:
        infection_deck.destroy_card(card)
        await ctx.send(f'{card.title()} has been Destroyed.')
        update_sheet(infection_deck.cards)
    except:
        await ctx.send('I don\'t think that\'s right')

#Epidemic command
@client.command(aliases=['darn', 'e'], brief='Epidemic')
async def epidemic(ctx):
    pan.increase_inf_rate()
    await ctx.send('1-Increase\n' +
                   f'The infection rate is now {pan.inf_rate[pan.inf_tracker]}')

    await ctx.send('2-It\'s wearing off.\n')
    while True:
        try:
            await ctx.send('Which card did you draw from Package 6?')
            msg = await client.wait_for('message')
            card = msg.content.lower()
            infection_deck.epidemic(str(card))
            print('Epidemic step 2 complete')
            break
        except:
            await ctx.send('Try that again')

    await ctx.send('3-Intensify\n'
                   'Shuffle the discard pile and place it on top of the deck.')
    update_sheet(infection_deck.cards)

@client.command(aliases = ['top', 't'],
                brief='Show which cards could be in the top X slots.')
async def top_cards(ctx):
    await ctx.send('How many cards should I check?')
    msg = await client.wait_for('message')
    x = int(msg.content)
    answer = infection_deck.top_x_cards(x)
    await ctx.send(answer)
    update_sheet(infection_deck.cards)

#See chance to hit each card
@client.command(aliases = ['odds', 'o'],
                brief='Odds of drawing a card in the top X cards.')
async def odds_top_cards(ctx):
    await ctx.send('How many cards should I check?')
    msg = await client.wait_for('message')
    x = int(msg.content)
    answer = infection_deck.create_probablility_dict(x)
    await ctx.send(answer)
    update_sheet(infection_deck.cards)

#Predict next infect cities step
@client.command(aliases = ['predict', 'prediction', 'p'],
                brief='Predict the next infect cities step.')
async def predict_infect_cities(ctx):
    answer = infection_deck.predict_next_infect_cities()
    await ctx.send(answer)
    update_sheet(infection_deck.cards)

#Change spreadsheet data to match dataframe
def update_sheet(deck):
    cards_df.update(deck)
    cards_df.to_csv('pandemic sheet.csv')
    sm.update_spreadsheet(cards_df)
client.run(TOKEN)
