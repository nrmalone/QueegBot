import discord
import auth
from discord.ext import commands

import jukebox
import rng
import cards
import customize
import chat
import bingo

client = commands.Bot(command_prefix='~', intents = discord.Intents.all())
cogs = []

#import classes into cogs object and add them to the bot's client
cogs += [jukebox]
cogs += [rng]
cogs += [cards]
cogs += [customize]
cogs += [chat]
cogs += [bingo]

for i in range(len(cogs)):
    cogs[i].setup(client)

#use auth.py so we don't leak any important tokens
client.run(auth.botToken)