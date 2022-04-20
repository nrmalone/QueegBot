import discord
import auth
from discord.ext import commands
import jukebox

client = commands.Bot(command_prefix='~', intents = discord.Intents.all())

cogs = [jukebox]
for i in range(len(cogs)):
    cogs[i].setup(client)

client.run(auth.botToken)