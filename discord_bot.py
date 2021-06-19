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

@client.command(aliases = ['start'])
async def start_game(ctx):
    pan.start_game(cards_df)
    await ctx.send('Game started!')

@client.command(aliases=['discard', 'infect'])

async def flip(ctx, *, card):
    await ctx.send(infection_deck.discard_top(card))
    await ctx.send('Infection Discard Pile:\n' + \
                    str(infection_deck.discard_list))

@client.command(aliases=['innoculate', 'package', 'exile'])
async def inoculate(ctx, *, card):
    infection_deck.inoculate(card)
    await ctx.send(f'{card.title()} was inoculated.\n'
                   'Package 6 Contents: ' +
                   str(infection_deck.package_list) +
                   '\nInfection Discard Pile: ' +
                   str(infection_deck.discard_list))

@client.command(aliases=['wear', 'unoculate'])
async def wear_off(ctx, *, card):
    infection_deck.wear_off(card)
    await ctx.send(f'{card.title()}\'s inoculation wore off.\n'
                   'Package 6 Contents: ' +
                   str(infection_deck.package_list) +
                   '\nInfection Discard Pile: ' +
                   str(infection_deck.discard_list))

@client.command(aliases = ['destroy', 'trash'])
async def destroy_card(ctx, *, card):
    infection_deck.destroy_card(card)
    await ctx.send(f'{card.title()} has been Destroyed.')

@client.command()
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

@client.command(aliases = ['top'])
async def top_cards(ctx):
    await ctx.send('How many cards should I check?')
    msg = await client.wait_for('message')
    x = int(msg.content)
    answer = infection_deck.top_x_cards(x)
    await ctx.send(answer)

@client.command(aliases = ['odds'])
async def odds_top_cards(ctx):
    await ctx.send('How many cards should I check?')
    msg = await client.wait_for('message')
    x = int(msg.content)
    answer = infection_deck.create_probablility_dict(x)
    await ctx.send(answer)

@client.command(aliases = ['predict', 'prediction'])
async def predict_infect_cities(ctx):
    answer = infection_deck.predict_next_infect_cities()
    await ctx.send(answer)

client.run(TOKEN)
