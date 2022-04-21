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
            msg += f"\t{i+1}.\t{game}\n"
        await ctx.send(msg, delete_after=60)


def setup(client):
    client.add_cog(cards(client))