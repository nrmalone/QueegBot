import random
import discord
from discord.ext import commands

class cards(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def cards(self, ctx):
        """
        Provides the user (via a Discord message) of which card games
        are available in this module (MANUALLY EDITED)
        """
        games = ["Poker", "Blackjack", "Speed"]
        msg = "Available games:\n"
        for i, game in enumerate(games):
            msg += f"\t{i+1}. {game}\n"
        await ctx.send(msg, delete_after=60)
    
    # TODO: Move this command to a newly created "customize.py"
    @commands.command()
    
    async def update(self, ctx, game_input):
        """
        Allows the user to update the bot user's
        "Playing {game}" status text
        """
        if len(game_input) > 40:
            ctx.send(str("CALM THE FUCK DOWN, MAAAAAN!!!"))
            game_input = f"LoL with {str(ctx.author)[:-5]}"
        game = discord.Game(str(game_input))
        await self.client.change_presence(activity=game)

def setup(client):
    client.add_cog(cards(client))