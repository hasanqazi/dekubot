import discord
import youtube_dl
from discord.ext import commands
import random

TOKEN = 'MzY0NDk2NjE4NzIxOTAyNTky.DLVQ2g.4bdaRbygvmKy57jrG83fP-Ou_6o'

client = commands.Bot(command_prefix = 'deku ')

players = {}
queues = {}

insults = [
    "to be a fuckboy you need to be, you know, fuckable.",
    "if I were a school shooter I'd go for yours first.",
    "you're impossible to underestimate.",
    "if you were an inanimate object, you'd be a participation trophy.",
    "you're not the dumbest person on the planet, but you sure better hope he doesn't die.",
    "you're kinda like Rapunzel except instead of letting down your hair you let down everyone in your life.",
    "you are like the end piece of bread in a loaf, everyone touches you but no one wants you.",
    "were you born a cunt, or is it something you have to recommit yourself to every morning?",
    "words can't describe your beauty...... but numbers can 1/10",
    "you're objectively unattractive.",
    "Mr. Rogers would be disappointed in you.",
    "You look like an open autopsy",
    "I envy people who have never met you.",
    "don't let that extra chromosome bring you down.",
    "it's better to let someone think you are an Idiot than to open your mouth and prove it.",
    "two wrongs don't make a right, take your parents as an example.",
    "your family tree must be a cactus because everybody on it is a prick.",
    "if laughter is the best medicine, your face must be curing the world.",
    "I wasn't born with enough middle fingers to let you know how I feel about you.",
    "stupidity is not a crime so you are free to go.",
    "you are proof that evolution CAN go in reverse.",
    "oh, what? Sorry. I was trying to imagine you with a personality.",
    "I'm not saying I hate you, but I would unplug your life support to charge my phone.",
    "roses are red, violets are blue, I have 5 fingers, the 3rd ones for you.",
    "if you are going to be two faced, at least make one of them pretty.",
]

def check_queue(id):
    if queues[id] != []:
        player = queues[id].pop(0)
        players[id] = player
        player.start()

@client.event
async def on_ready():
    print("Connection established.")

@client.command(pass_context=True)
async def roast(ctx, name):
    insult = random.randint(0, (len(insults)-1))
    await client.say(name + ', ' + insults[insult])

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