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
    
    #roll <# of dice> <type of die>
    @commands.command()
    async def roll(self,ctx,diceQuantity=None,diceType=None):
        roll = 0
        if 'd' in ctx.message.content:
            roll_text = (ctx.message.content[6:]).split('d')
            diceQuantity = str(roll_text[0].strip())
            diceType = str(roll_text[1].strip())
        if str.isnumeric(diceQuantity):
            for die in range(1, int(diceQuantity)):
                roll += random.randint(1,int(diceType))
        await ctx.send(":game_die: " + (diceQuantity + "d" + diceType + " :arrow_right: " + str(roll)), delete_after=30)

def setup(client):
    client.add_cog(rng(client))