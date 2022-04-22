import discord
from discord.ext import commands
import youtube_dl
from pathlib import Path

class jukebox(commands.Cog):
    def __init__(self, client):
        self.client = client

    # join
    # joins user's vc
    @commands.command()
    async def join(self,ctx):
        # if author.voice doesn't detect user is in a vc, send message telling them to join vc
        if ctx.author.voice is None:
            await ctx.send("Connect to a voice channel, " + ctx.author.display_name + "!!")
        if not ctx.author.voice is None:
            voice_channel = ctx.author.voice.channel
        # connect to a vc if not already connect else move to user's vc
        if ctx.voice_client is None:
            await voice_channel.connect()
            await ctx.send("I'm here, MAN!!", delete_after=10)
        else:
            await ctx.voice_client.move_to(voice_channel)
            await ctx.send("Who moved me, MAN!?", delete_after=10)

    
    # leave
    # leaves voice channel
    @commands.command()
    async def leave(self,ctx):
        await ctx.voice_client.disconnect()

    # play
    # plays audio thru youtube url (requires a few seconds to download)
    @commands.command()
    async def play(self,ctx,url):
        # have bot stop playing audio and provide bot with settings for playing audio
        ctx.voice_client.stop()
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        YDL_OPTIONS = {'format':"bestaudio"}
        vc = ctx.voice_client
        
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2,**FFMPEG_OPTIONS)
            vc.play(source)
    
    # pause
    @commands.command()
    async def pause(self,ctx):
        ctx.voice_client.pause()
        await ctx.send("whoa :pause_button:", delete_after=10)

    # unpause
    @commands.command()
    async def unpause(self,ctx):
        ctx.voice_client.resume()
        await ctx.send("soda :arrow_forward:", delete_after=10)

    # stop
    @commands.command()
    async def stop(self,ctx):
        ctx.voice_client.stop()
        await ctx.send("u were right :skull_crossbones:", delete_after=10)

    """
    Decided we can try an all-encompassing sfx that checks when we add new mp3's to assets directory
    """
    # snore
    @commands.command()
    async def sfx(self,ctx,sfx):
        if ctx.author.voice is None:
            await ctx.send("Connect to a voice channel, " + ctx.author.display_name + "!!")
        if not ctx.author.voice is None:
            voice_channel = ctx.author.voice.channel
        # connect to a vc if not already connect else move to user's vc
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)

        if Path(__file__.replace('jukebox.py',('/assets/' + sfx + '.mp3'))).is_file():
            sound = discord.FFmpegPCMAudio(source='./assets/'+ sfx +'.mp3', executable='./assets/ffmpeg.exe')
            vc = ctx.voice_client
            vc.play(sound)
        else:
            await ctx.send("ain't no fuckin ~~point~~ *audio*")

def setup(client):
    client.add_cog(jukebox(client))