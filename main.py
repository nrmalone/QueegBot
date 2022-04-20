import discord
import auth
from discord.ext import commands
import jukebox
import rng

client = commands.Bot(command_prefix='~', intents = discord.Intents.all())

cogs = [jukebox]
cogs += [rng]
for i in range(len(cogs)):
    cogs[i].setup(client)

client.run(auth.botToken)