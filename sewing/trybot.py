# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/nbs/trybot.ipynb (unless otherwise specified).

__all__ = ['get_default_channels', 'retrieve', 'get_all_messages', 'on_ready', 'register', 'roll', 'choose', 'repeat',
           'cool', 'description', 'bot', 'now', 'yesterday']

# Cell
import sewing
import discord
import datetime

# Cell
# This example requires the 'members' privileged intents

import discord
from discord.ext import commands
import random

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''

bot = commands.Bot(command_prefix='>>', description=description)

now = datetime.datetime.now()
yesterday = now - datetime.timedelta(days=1)


def get_default_channels():
    return ['873950891663839245']


async def retrieve(messagable, after=None, **kwargs):
    '''
    messagable = thread or channel
    See other kwargs
    https://discordpy.readthedocs.io/en/stable/api.html#discord.TextChannel.history
    '''

    after = after or yesterday
    messages = await messagable.history(after=after, **kwargs).flatten()
    return messages

async def get_all_messages():
    messages_by_thread = {}
    for chan_id in get_default_channels():
        chan = await bot.fetch_channel(chan_id)
        print(chan.threads)
        for thread in chan.threads:
            messages = await retrieve(thread)
            print('=========')
            for msg in messages:
                print(msg)
            messages_by_thread[thread] = messages
    return messages_by_thread


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


@bot.command()
async def register(ctx, email: str):
    """Registers a user to receive email updates"""
    print(ctx)
    #import pdb; pdb.set_trace()
    await ctx.send("You're signed up at {}.  If thats the wrong email just register again.".format(email))

@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)

@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))

@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)


@bot.group()
async def cool(ctx):
    """Says if a user is cool.
    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await ctx.send(f'No, {ctx.subcommand_passed} is not cool')

@cool.command(name='bot')
async def _bot(ctx):
    """Is the bot cool?"""
    await ctx.send('Yes, the bot is cool.')

# Cell
if sewing.is_main(globals()):
    sewing.start_log()
    #client_secret = 'HN3In0Y-zWsb3arHkEnayIILiqAE5iyc'
    #client_id = '873958608956710912'

    token = 'ODczOTU4NjA4OTU2NzEwOTEy.YQ__YQ.8xrXGfsY3nN-lwiNT_gqEDrXedw'
    #client.run(token)
    bot.run(token)