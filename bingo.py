from re import X
import discord
from discord.ext import commands
import random

class bingo(commands.Cog):
    def __init__(self,client):
        self.client = client
    
    # bingocard
    @commands.command()
    async def bingocard(self,ctx):
        x = 0
        for space in range(1,25):
            card += x
        await ctx.author.send(str(card))

def setup(client):
    client.add_cog(bingo(client))