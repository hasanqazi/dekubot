import discord
import youtube_dl
from discord.ext import commands
import random

TOKEN = ''

client = commands.Bot(command_prefix = 'deku ')

players = {}
queues = {}

def check_queue(id):
    if queues[id] != []:
        player = queues[id].pop(0)
        players[id] = player
        player.start()

@client.event
async def on_ready():
    print("Connection established.")

@client.command(pass_context=True)
async def mock(ctx, text):
    smp = "".join( random.choice([k.upper(), k ]) for k in text )
    await client.say(smp)
    await client.send_file(ctx.message.channel, 'mock.jpg')

@client.event
async def on_message_delete(message):
    author = message.author
    content = message.content
    await client.send_message(client.get_channel('500464557307985920'), '{}: {}'.format(author, content))

@client.command(pass_context=True)
async def greentext(ctx, text):
    await client.say('```css\n' + str(text) + '\n```')

@client.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.voice_channel
    await client.join_voice_channel(channel)

@client.command(pass_context=True)
async def leave(ctx):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    await voice_client.disconnect()

@client.command(pass_context=True)
async def play(ctx, url):
    channel = ctx.message.author.voice.voice_channel
    await client.join_voice_channel(channel)
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url)
    players[server.id] = player
    player.start()

@client.command(pass_context=True)
async def pause(ctx):
    id = ctx.message.server.id
    players[id].pause()

@client.command(pass_context=True)
async def skip(ctx):
    id = ctx.message.server.id
    players[id].stop()
    player = queues[id].pop(0)
    players[id] = player
    player.start()

@client.command(pass_context=True)
async def stop(ctx):
    id = ctx.message.server.id
    players[id].stop()

@client.command(pass_context=True)
async def resume(ctx):
    id = ctx.message.server.id
    players[id].resume()

@client.command(pass_context=True)
async def queue(ctx, url):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))

    if server.id in queues:
        queues[server.id].append(player)
    else:
        queues[server.id] = [player]
    await client.say('Video queued.')

client.run(TOKEN)
