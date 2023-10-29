import discord
from discord.ext import commands
import yt_dlp as youtube_dl
import asyncio
from random import choice
import rick
from datetime import datetime
import argparse
parser = argparse.ArgumentParser(description="OBot discord bot")
parser.add_argument('--token', help='Token Discord')
parser.add_argument('--client_id', help="Client ID for invitation links if not set the invite command will be disabled")
args = parser.parse_args()
token = args.token
client_id = args.client_id

if client_id == None or client_id == "null":
    print("No Client ID specified the invite command will be disabled")
else:
    print("Client ID was set to " + client_id)

if args.token == "":
    print("No token Specified Syntaxe : python Obot.py --token <your token>")
    exit(52)
else:
    if token == 'default_token':
        print("the token has not been change actual token : " + token)
        exit(51)
    else:
        print("actual discord token :", token)
    

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.messages = True
intents.presences = True
ytdl = youtube_dl.YoutubeDL()
bot = commands.Bot(command_prefix="-", intents=intents)
musics = {}




class Video:
    def __init__(self, link):
        video = ytdl.extract_info(link, download=False)
        video_format = video['requested_formats']
        self.url = video["webpage_url"]
        self.stream_url = video_format[1]['url']


@bot.event
async def on_member_join(member):
    print(f'{member} has joined the server')
    await member.add_roles(discord.utils.get(member.guild.roles, name="😀 [Utilisateur] 😀"))
    print(f"user role given to  {member}")
    await bot.get_channel(818742029881180201).send(f"Bienvenu(e) a toi sur se serveur @{member}.")
    print(f"welcome message send for {member}")


@bot.event
async def on_ready():
    print(f'logged in as {bot.user} ')


@bot.command()
async def time(ctx):
    print("time send")
    channel = ctx
    await channel.send("il est " + datetime.now().strftime("%H") + " heures " + datetime.now().strftime("%M") + " minutes.")


@bot.command(aliases=['crédits'])
async def credits(ctx):
    channel = ctx
    await channel.send(
        "OBot was dev by OXipro and totally writen in Python. \n the Github Project link is : coming soon.")
    print("crédits send")


@bot.command()
async def resume(ctx):
    client = ctx.guild.voice_client
    if client.is_paused():
        client.resume()


@bot.command()
async def pause(ctx):
    client = ctx.guild.voice_client
    if not client.is_paused():
        client.pause()


@bot.command()
async def invite(ctx):
    print("invite on server requested")
    if client_id == None or client_id == "null":
        print("No Client ID not specified invite is Disabled")
        await ctx.send("Je ne peux pas vous donner d'invitation car la Valeur de Client ID au démarage na pas été spécifié")
    else:
        await ctx.send("Voici le lien d'invitation de OBot : \n " + discord.utils.oauth_url(client_id, permissions=discord.Permissions(administrator=True)) + "\n a bientot sur votre serveur :/")
        print("invite on server send")

@bot.command()
async def leave(ctx):
    print("requesting to leave voice channel")
    client = ctx.guild.voice_client
    await client.disconnect()
    print("disconnected for discord voice channel")
    musics[ctx.guild] = []


def play_song(client, queue, song):
    print("cc " + song.stream_url)
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(song.stream_url,before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"))
    def next(_):
        if len(queue) > 0:
            new_song = queue[0]
            del queue[0]
            play_song(client, queue, new_song)
        else:
            asyncio.run_coroutine_threadsafe(client.disconnect(), bot.loop)

    client.play(source, after=next)


@bot.command()
async def play(ctx, url):
    failedrickrolllist = ['Hahaha raté pas de chance /:', 'Non merci !!!', "ouf, j'ai failli clicker dessus !!!!",
                          'Bien bien essayé', 'un peux trop osé', 'nice try obiwan', 'Nulos nul', "n'y pense meme pas",
                          'vade retro satanas']
    print("requesting to play " + url)
    client = ctx.guild.voice_client
    if rick.find(url=url):
        await ctx.send(choice(failedrickrolllist))
        print("failed to play its a rickroll !!!!!!")
    else:
        if client and client.channel:
            video = Video(url)
            print(video)
            musics[ctx.guild].append(video)
            print("added " + url + " to queue")
            ctx.send(url + " a été ajouté a la playlist")
        else:
            channel = ctx.author.voice.channel
            video = Video(url)
            stream_url = video.stream_url
            musics[ctx.guild] = []
            client = await channel.connect()
            await ctx.send(f"Je lance : {video.url}")
            print("playing " + url)
            play_song(client, musics[ctx.guild], video)


bot.run(args.token)
# print(rickrolldetector.find(url="https://www.youtube.com/watch?v=zSzFHxOkCfo"))
