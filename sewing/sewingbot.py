# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/nbs/sewingbot.ipynb (unless otherwise specified).

__all__ = ['description', 'bot', 'guilds', 'get_all_channel_content', 'get_all_guild_content', 'sew_threads',
           'on_ready', 'register', 'unregister', 'email', 'summarize', 'suggest', 'helpme']

# Cell
from pprint import pprint
import json
import discord
import logging
import datetime

from discord.ext import tasks, commands

import sewing
import sewing.db as db
from .notify import Retriever, send_content

# Cell

description = '''Summarize threads and send as an email'''
bot = commands.Bot(command_prefix='!', description=description)

# Cell
async def guilds():
    guilds = db.guilds()
    guild_objects = []
    for guild_d in guilds:
        guild_id = guild_d['guild']['id']
        guild = await bot.fetch_guild(guild_id)
        guild_objects.append(guild)
    return guild_objects

async def get_all_channel_content(channels):
    retriever = Retriever()
    channels_content = {}
    for channel_d in channels:
        channel_id = channel_d['channel']['id']
        channel_obj = await bot.fetch_channel(int(channel_id))
        #{thread: [messages]}
        messages = await retriever.get_all_messages_in_channel(channel_obj)
        #print(json.dumps(messages))
        channels_content[channel_obj] = messages
    return channels_content

async def get_all_guild_content(all_guilds):
    guild_content = {}
    for guild in all_guilds:
        channels = db.summarized_channels(guild, names_only=False)
        channels_content = await get_all_channel_content(channels)
        guild_content[guild] = channels_content
    return guild_content

@tasks.loop(minutes=1, count=5)
async def sew_threads():
    print(sew_threads.current_loop)
    all_guilds = await guilds()
    guild_content = await get_all_guild_content(all_guilds)
    print(guild_content)

    for guild, content in guild_content.items():
        send_content(content, guild)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    db.ensure_unique_nodes()
    for guild in bot.guilds:
        db.ensure_guild(guild)
    await sew_threads()
    sew_threads.start()

# Cell

@bot.command(description="Registers you to receive email updates")
async def register(ctx):
    guild = ctx.guild
    author = ctx.author

    if guild is None:
        await author.send("I can't tell which guild you're registering for.  `!register` from a guild channel")
        return None
    print(guild, ctx.author.mutual_guilds)
    resp = db.register_user(author, guild)
    record = db.get_email(author)['email']
    email_text = 'We have no email address for you'

    if record:
        email_text = 'Your email is {}'.format(record)
    await author.send("You're signed up. {email_text}.  `!email me@email.com` to change your email address".format(
            email_text=email_text))

@bot.command(description="You stop getting email updates")
async def unregister(ctx):
    guild = ctx.guild
    author = ctx.author

    if guild is None:
        await author.send("I can't tell which guild you're unregistering for.  `!unregister` from a guild channel")
        return None
    resp = db.unregister_user(author, guild)
    await ctx.send("Was it something I said?  (You'll stop getting summary emails from me).")

@bot.command(description="Add your email address")
async def email(ctx, address:str):
    author = ctx.author
    resp = db.set_email(author, address)
    await author.send("Email address recorded")


# Cell

@bot.command(description="START or STOP threads on this channel from being summarized")
async def summarize(ctx, cmd:str=''):
    guild = ctx.guild
    channel = ctx.channel

    cmd = cmd.upper()

    if cmd not in ('START', 'STOP'):
        await ctx.send("Usage: `!summarize start` or `!summarize stop`")

    if cmd=='START':
        resp = db.add_channel(channel, guild)

    elif cmd=='STOP':
        resp = db.remove_channel(channel, guild)

    all_channels = db.summarized_channels(guild, names_only=True)
    if all_channels:
        msg = "Channels being summarized are: {}".format(','.join(all_channels))
    else:
        msg = "No channels are being summarized"
    await ctx.send(msg)

# Cell

@bot.command()
async def suggest(ctx, *args):
    user = ctx.author
    db.add_suggestion(user, *args)
    await ctx.send("Thanks for the suggestion.  Its been passed along to the bot's developer")

# Cell

@bot.command("how")
async def helpme(ctx):
    help_text='''
You can `!register` for email updates of important threads.
When you do, I'll DM you so you can set your email address `!email my@address.com`.
`!unregister` to stop getting email updates.
You can also `!suggest your good ideas` to the devs of this bot
    '''
    await ctx.send(help_text)

# Cell
import os
if sewing.is_main(globals()):
    logger = sewing.start_log()
    logger.setLevel(logging.INFO)

    token = os.environ['DISCORD_TOKEN']
    #client.run(token)
    bot.run(token)