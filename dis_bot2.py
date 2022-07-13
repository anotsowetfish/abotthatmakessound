import discord
from discord import voice_client
from discord.ext import commands
import playlist as yt
import discord
from discord.ext import tasks

bot = commands.Bot(command_prefix='!')
FFmpeg_executable = 'F:\Programming\drivers\FFMPEG/ffmpeg-4.4.1-essentials_build/bin/ffmpeg.exe'


playlist = yt.Playlist()

# when bot ready connect to discord servers
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

# when the play command is called
@bot.command(aliases = ['p','P'])
async def append_song(ctx,message):
    # channel : voice channel of user that called command
    channel = ctx.author.voice.channel
    # voice : actually dont know
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    # player : the speaker in which audio files are played
    player = voice_client.VoiceClient

    playlist.set_ctx(ctx)
    playlist.set_channel(channel)
    playlist.set_voice(voice)
    playlist.set_player(player)
    playlist.set_discord(discord)

    # connects bot to voice channel if not already connected
    if voice == None:
        await channel.connect()
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        playlist.set_voice(voice)
    #dictates accepted link domain
    if not "youtube" and not "youtu.be" in message:
        text = ctx.channel
        await text.send('{}, onbekende link'.format(ctx.author.name.upper()))
        return

    await playlist.append(link=message)
    await playlist.play()

@bot.command(aliases = ['s','S'])
async def skip(ctx):
    voice_client.VoiceClient.stop(playlist.voice)

@bot.command(aliases = ['pt','PT'])
async def playtop(ctx,message):
    await playlist.append_top(message)

@bot.command(aliases = ['ps','PS'])
async def playskip(ctx,message):
    await playlist.append_top(message)
    await skip(ctx)



bot.run('OTExNjQ2MjkxNjUyNjY5NDkx.YZkaxQ.QuyGBsxcIQ-nInVpfCdqwhS9x2E')