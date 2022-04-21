import random
import discord
from discord.ext import commands
from asyncio import TimeoutError as TE

class cards(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    async def cards(self, ctx):
        """
        Provides the user a list of functional games to play (MANUALLY EDITED),
        takes a choice in that same channel, and calls that game's function to play
        """
        async def poker(self, ctx):
            print("Poker selected successfully")
    

        async def blackjack(self, ctx):
            print("Blackjack selected successfully")
        

        async def speed(self, ctx):
            print("Speed selected successfully")
        
        game_dict = {"Poker" : poker, "Blackjack": blackjack, "Speed": speed}
        choice_dict = {}
        msg = "Available games:\n"
        for i, game in enumerate(game_dict.keys()):
            msg += f"\t{i+1}.\t{game}\n"
            choice_dict[str(i+1)] = game
        for num in choice_dict:
            print(f"{num}: {choice_dict[num]}")
        msg += "Enter a # to make your choice."
        await ctx.send(msg, delete_after=10)
        og_author, og_channel = ctx.author, ctx.channel
        def check(msg):
            """
            Checks that the original user is responding, 
            in the same channel, and with a valid choice
            from the games listed
            """
            return msg.content in choice_dict.keys() and msg.channel == og_channel and msg.author == og_author
        try:
            choice = await self.client.wait_for('message', timeout=10, check=check)
        except TE:
            await ctx.send("You didn't even pick one, MAN!!!", delete_after=10)
            return
        game = str(choice_dict[choice.content])
        await ctx.send("You chose: " + game, delete_after=5)
        await game_dict[game](self, ctx)


def setup(client):
    client.add_cog(cards(client))