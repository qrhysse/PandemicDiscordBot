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
    sm.worksheet.format('I5:J6', {
                    "backgroundColor": {"red": 1.0, "green": 0.0, "blue": 0.0}})

@client.command()
async def stop(ctx):
    sm.worksheet.format('I5:J6', {
                    "backgroundColor": {"red": 1.0, "green": 1.0, "blue": 1.0}})

@client.command(aliases = ['start'], brief='Reset the deck for a new game.')
async def start_game(ctx):
    reset_deck = pan.start_game(infection_deck)
    update_sheet(reset_deck.cards)
    infection_deck.reset(cards_df, infection_deck.type)
    print(infection_deck.cards.head())
    await ctx.send(f'Game started!')

@client.command(brief='Ckeck the current state of the game')
async def state(ctx):
    await ctx.send(f'Package 6 Contents: {len(infection_deck.package_list)} cards\n' +
    str(infection_deck.package_list) +
    f'\nInfection Discard Pile: {len(infection_deck.discard_list)} cards\n' +
    str(infection_deck.discard_list))

@client.command(aliases=['discard', 'infect'],
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

@client.command(aliases=['innoculate', 'package', 'exile'],
                brief='Move a card from Discard to Package 6')
async def inoculate(ctx, *, card):
    try:
        infection_deck.inoculate(card)
        await ctx.send(f'{card.title()} was inoculated.\n'
            f'Package 6 Contents: {len(infection_deck.package_list)} cards\n' +
            str(infection_deck.package_list) +
            f'\nInfection Discard Pile: {len(infection_deck.discard_list)} cards\n' +
            str(infection_deck.discard_list))
        update_sheet(infection_deck.cards)
    except:
        await ctx.send('I don\'t think that\'s right')

@client.command(aliases=['wear', 'unoculate'],
                brief='Move a card from Package 6 to Discard')
async def wear_off(ctx, *, card):
    try:
        infection_deck.wear_off(card)
        await ctx.send(f'{card.title()}\'s inoculation wore off.\n'
            f'Package 6 Contents: {len(infection_deck.package_list)} cards\n' +
            str(infection_deck.package_list) +
            f'\nInfection Discard Pile: {len(infection_deck.discard_list)} cards\n' +
            str(infection_deck.discard_list))
        update_sheet(infection_deck.cards())
    except:
        await ctx.send('I don\'t think that\'s right')

@client.command(aliases = ['destroy', 'trash'],
                brief='Move a card from Discard to Trash')
async def destroy_card(ctx, *, card):
    try:
        infection_deck.destroy_card(card)
        await ctx.send(f'{card.title()} has been Destroyed.')
        update_sheet(infection_deck.cards)
    except:
        await ctx.send('I don\'t think that\'s right')

@client.command(aliases=['darn'], brief='Epidemic')
async def epidemic(ctx):
    pan.increase_inf_rate()
    await ctx.send('1-Increase\n' +
                   f'The infection rate is now {pan.inf_rate[pan.inf_tracker]}')
    await ctx.send('2-It\'s wearing off.\n'
                   'Which card did you draw from Package 6?')
    msg = await client.wait_for('message')
    card = msg.content.lower()
    infection_deck.epidemic(str(card))
    await ctx.send('3-Intensify\n'
                   'Shuffle the discard pile and place it on top of the deck.')
    update_sheet(infection_deck.cards)

@client.command(aliases = ['top'],
                brief='Show which cards could be in the top X slots.')
async def top_cards(ctx):
    await ctx.send('How many cards should I check?')
    msg = await client.wait_for('message')
    x = int(msg.content)
    answer = infection_deck.top_x_cards(x)
    await ctx.send(answer)
    update_sheet(infection_deck.cards)

@client.command(aliases = ['odds'],
                brief='Odds of drawing a card in the top X cards.')
async def odds_top_cards(ctx):
    await ctx.send('How many cards should I check?')
    msg = await client.wait_for('message')
    x = int(msg.content)
    answer = infection_deck.create_probablility_dict(x)
    await ctx.send(answer)
    update_sheet(infection_deck.cards)

@client.command(aliases = ['predict', 'prediction'],
                brief='Predict the next infect cities step.')
async def predict_infect_cities(ctx):
    answer = infection_deck.predict_next_infect_cities()
    await ctx.send(answer)
    update_sheet(infection_deck.cards)

def update_sheet(deck):
    cards_df.update(deck)
    cards_df.to_csv('pandemic sheet.csv')
    sm.update_spreadsheet(cards_df)
client.run(TOKEN)
