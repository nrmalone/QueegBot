import discord
from discord.ext import commands

class customize(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def update(self, ctx, game_input):
        """
        Allows the user to update the bot user's
        "Playing {game}" status text
        """
        if len(game_input) > 40:
            await ctx.send(str("CALM THE FUCK DOWN, MAAAAAN!!!"), delete_after=10)
            game_input = f"LoL with {str(ctx.author)[:-5]}"
        game = discord.Game(str(game_input))
        await self.client.change_presence(activity=game)


def setup(client):
    client.add_cog(customize(client))