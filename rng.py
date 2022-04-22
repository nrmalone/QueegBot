import discord
from discord.ext import commands
import random

class rng(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    async def coin(self,ctx):
        """
        Allows users to flip a coin with command "coin"
        Sends heads or tails message according to result
        """
        await ctx.message.delete
        coin = random.randint(0,1)
        if coin == 0:
            await ctx.send(":coin: heads", delete_after=30)
        if coin == 1:
            await ctx.send(":coin: tails", delete_after=30)
    

    @commands.command()
    async def roll(self,ctx,diceQuantity=None,diceType=None):
        """
        Allows users to roll 1 or more dice of a specified length
        No provided dice count defaults to 1
        
        "roll <# of dice> <type of die>" 
        or 
        "roll <# of dice>d<type of die>"
        """
        await ctx.message.delete()
        roll = 0
        if 'd' in ctx.message.content:
            roll_text = (ctx.message.content[6:]).split('d')
            diceQuantity = str(roll_text[0].strip())
            diceType = str(roll_text[1].strip())
        if not str.isnumeric(diceQuantity):
            diceQuantity = '1'
        if not str.isnumeric(diceType):
            await ctx.send("Learn to TYPE properly, MAN!!!", delete_after=10)
            return
        for die in range(int(diceQuantity)):
            die_roll = random.randint(1,int(diceType))
            roll += die_roll
        await ctx.send(":game_die: " + (diceQuantity + "d" + diceType + " :arrow_right: " + str(roll)), delete_after=60)

    @commands.command()
    async def rng(self, ctx, *args):
        """
        Generates & sends a random number specified
        by either 1 number, or by a range of 2 given numbers

        "rng <max #>"
        or
        "rng <min #> <max #>"
        """
        await ctx.message.delete()
        try:
            start = 1
            stop = int(args[0])
            if len(args) > 1:
                start = int(args[0])
                stop = int(args[1])
            num = random.randint(start, stop)
            await ctx.send(":1234:  " + str(num) + "  :1234:", delete_after=60)
        except:
            await ctx.send("Learn to TYPE properly, MAN!!!", delete_after=10)


def setup(client):
    client.add_cog(rng(client))