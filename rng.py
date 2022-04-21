import discord
from discord.ext import commands
import random

class rng(commands.Cog):
    def __init__(self, client):
        self.client = client

    # coin
    @commands.command()
    async def coin(self,ctx):
        coin = random.randint(0,1)
        if coin == 0:
            await ctx.send(":coin: heads", delete_after=30)
        if coin == 1:
            await ctx.send(":coin: tails", delete_after=30)
    
    #dice <# dices> <type of die>
    @commands.command()
    async def dice(self,ctx,diceQuantity,diceType):
        roll = 0
        if str.isnumeric(diceQuantity):
            for die in range(1, int(diceQuantity)):
                roll += random.randint(1,int(diceType))
        await ctx.send(":game_die: " + (diceQuantity + "d" + diceType + " :arrow_right:" + str(roll)), delete_after=30)

def setup(client):
    client.add_cog(rng(client))