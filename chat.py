import discord
from discord.ext import commands
from asyncio import TimeoutError as TE
from time import sleep

class chat(commands.Cog):
    def __init__(self, client):
        self.client = client
    

    @commands.command()
    async def claymore(self, ctx):
        """
        Places a friendly M18 A1 APERSMINE for
        users in the specified text channel
        """
        await ctx.message.delete()
        await ctx.send(file=discord.File(fp='.\claymore.png'), delete_after=60)
        try:
            # Waits to see if the mine is triggered
            msg = await self.client.wait_for('message', timeout=5)
        except TE:
            # Informs the chatters that the claymore is now inactive
            await ctx.send("You're safe for now...", delete_after=55)
            return
        # If the mine is triggered, attacks the chatter with a variety of punishments
        if msg.author.id == self.client.user.id:
            await ctx.send("Nice try, MAN!!!", delete_after=10)
            return
        await ctx.send(str(msg.author.display_name + " IS ONE DUMB MOTHERFUCKER!!!"), delete_after=60)
        prev_channel = ctx.author.voice.channel
        await msg.author.edit(mute=True, deafen=True, voice_channel=ctx.message.guild.afk_channel, reason='claymore')
        # Allows the user (or any others in the call) to save the victim by reacting to a message
        try:
            await self.client.wait_for('reaction_add', timeout=10)
        except TE:
            pass
        await msg.author.edit(mute=False, deafen=False, voice_channel=prev_channel)

def setup(client):
    client.add_cog(chat(client))