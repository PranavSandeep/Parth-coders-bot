import asyncio
import json
import discord
from better_profanity import profanity
from discord.ext import commands
import youtube_dl
from discord.ext.commands import has_permissions
import YtSong_searcher
import os

Token = os.getenv("VARIABLE_NAME")


client = commands.Bot(command_prefix="$")

queue = []


@client.event
async def on_ready():
    print("The bot is now ready for use")

    @client.event
    async def on_message(message):

        if message.author == client.user:
            return
        if isinstance(message.channel, discord.channel.DMChannel):
            return

        if profanity.contains_profanity(message.content):
            await message.channel.send(f'Stop swearing, {str(message.author.mention)}, idiot')
            await message.delete()

        if "$name" in message.content:
            await message.channel.send(f'{message.author.mention}')

        if not message.author.bot:
            print('function load')
            with open('users', 'r') as f:
                users = json.load(f)
                print('file load')
            await update_data(users, message.author)
            await add_experience(users, message.author, 4)
            await level_up(users, message.author, message)

            with open('users', 'w') as f:
                json.dump(users, f)

        await client.process_commands(message)


@client.event
async def on_member_join(member):
    with open('users', 'r') as f:
        users = json.load(f)

    await update_data(users, member)

    with open('users', 'w') as f:
        json.dump(users, f)


@client.command(help="Kicks the user form the server")
@has_permissions(administrator=True)
async def kick(ctx, Member: discord.Member, *, reason=None):
    await Member.kick(reason=reason)

    global ChannelId

    try:
        channel = client.get_channel(ChannelId)
        await channel.send(f'{ctx.author.mention} kicked {Member.mention}')

    except:
        guild = ctx.guild
        channel = await guild.create_text_channel("Mod Logs")
        ChannelId = channel.id
        await channel.send(f'{ctx.author.mention} kicked {Member.mention}')


@client.command(help="Bans the user form the server")
@has_permissions(administrator=True)
async def ban(ctx, Member: discord.Member, *, reason=None):
    await Member.ban(reason=reason)

    global ChannelId

    try:
        channel = client.get_channel(ChannelId)
        await channel.send(f'{ctx.author.mention} banned {Member.mention}')

    except:
        guild = ctx.guild
        channel = await guild.create_text_channel("Mod Logs")
        ChannelId = channel.id
        await channel.send(f'{ctx.author.mention} banned {Member.mention}')


@client.command(name='ping', help='This command returns the latency')
async def ping(ctx):
    await ctx.send(f'**Pong!** Latency: {round(client.latency * 1000)}ms')


async def update_data(users, user):
    if not f'{user.id}' in users:
        users[f'{user.id}'] = {}
        users[f'{user.id}']['experience'] = 0
        users[f'{user.id}']['level'] = 1


async def add_experience(users, user, exp):
    users[f'{user.id}']['experience'] += exp


async def level_up(users, user, message):
    with open('users', 'r') as g:
        levels = json.load(g)
    experience = users[f'{user.id}']['experience']
    lvl_start = users[f'{user.id}']['level']
    lvl_end = int(experience ** (1 / 4))
    if lvl_start < lvl_end:
        await message.channel.send(f'{user.mention} has leveled up to level {lvl_end}')
        users[f'{user.id}']['level'] = lvl_end


@client.command(help="Shows your level")
async def level(ctx, member: discord.Member = None):
    if not member:
        id = ctx.message.author.id
        with open('users', 'r') as f:
            users = json.load(f)
        lvl = users[str(id)]['level']
        await ctx.send(f'You are at level {lvl}!')
    else:
        id = member.id
        with open('users', 'r') as f:
            users = json.load(f)
        lvl = users[str(id)]['level']
        await ctx.send(f'{member} is at level {lvl}!')


@client.command()
async def hello(ctx):
    await ctx.send("Yo!")


@client.command(description="Mutes the specified user.", aliases=['mute'])
@commands.has_permissions(manage_messages=True)
async def Mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Degenerates")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Degenerates")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True,
                                          read_messages=True)
    embed = discord.Embed(title="Degenerates", description=f"{member.mention} was Unmuted ",
                          colour=discord.Colour.light_gray())
    embed.add_field(name="reason:", value=reason, inline=False)
    await ctx.send(embed=embed)
    await member.add_roles(mutedRole, reason=reason)
    await member.send(f" you have been muted from: {guild.name} reason: {reason}")

    global ChannelId

    try:
        channel = client.get_channel(ChannelId)
        await channel.send(f'{ctx.author.mention} muted {member.mention}')

    except:
        guild = ctx.guild
        channel = await guild.create_text_channel("Mod Logs")
        ChannelId = channel.id
        await channel.send(f'{ctx.author.mention} muted {member.mention}')


@client.command(description="Unmutes the specified user.", aliases=['unmute'])
@commands.has_permissions(manage_messages=True)
async def Unmute(ctx, member: discord.Member):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Degenerates")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Degenerates")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True,
                                          read_messages=True)
    embed = discord.Embed(title="Degenerates", description=f"{member.mention} was unmuted ",
                          colour=discord.Colour.light_gray())

    await ctx.send(embed=embed)
    await member.remove_roles(mutedRole)
    await member.send(f" you have been unmuted from: {guild.name}")

    global ChannelId

    try:
        channel = client.get_channel(ChannelId)
        await channel.send(f'{ctx.author.mention} unmuted {member.mention}')

    except:
        guild = ctx.guild
        channel = await guild.create_text_channel("Mod Logs")
        ChannelId = channel.id
        await channel.send(f'{ctx.author.mention} unmuted {member.mention}')


@client.command(help='Changes the prefix.')
async def ChangePrefix(ctx, Prefix):
    client.command_prefix = Prefix


@client.command(pass_context=True, help='This command purges(deletes) the amount of messages you tell it to')
@commands.has_permissions(administrator=True)
async def purge(ctx, limit: int):
    await ctx.channel.purge(limit=limit)

    global ChannelId

    try:
        channel = client.get_channel(ChannelId)
        await channel.send(f'{ctx.author.mention} cleared {limit} messages')

    except:
        guild = ctx.guild
        channel = await guild.create_text_channel("Mod Logs")
        ChannelId = channel.id
        await channel.send(f'{ctx.author.mention} cleared {limit} messages')


@client.command(name='remove', help='This command removes an item from the list')
async def remove(ctx, number):
    try:
        del (queue[int(number)])
        await ctx.send(f'Your queue is now `{queue}!`')

    except:
        await ctx.send('Your queue is either **empty** or the index is **out of range**')


def EndSong(ctx):
    os.remove("song.mp3")


@client.command()
async def play(ctx, *url: str):
    url = YtSong_searcher.GetVidId(url)
    queue.append(url)
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send(f"{url} added to queue!")
        return

    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
    try:
        await voiceChannel.connect()
    except:
        pass
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([queue[0]])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    del (queue[0])
    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=EndSong)


@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")


@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")


@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()


@client.command()
async def skip(ctx):
    if len(queue) != 0:
        await stop(ctx)

        await asyncio.sleep(1)

        await play(ctx, queue[0])

        RemovedSong = queue.pop(0)


    else:
        await ctx.send("There is nothing to skip!")


@client.command()
async def Queue(ctx):
    await ctx.send(queue)



client.run(Token)

# If you wish to securely hide your token, you can do so in a .env file.
# 1. Create a .env in the same directory as your Python scripts
# 2. In the .env file format your variables like this: VARIABLE_NAME=your_token_here
# 3. At the top of the Python script, import os
# 4. In Python, you can read a .env file using this syntax:
# token = os.getenv(VARIABLE_NAME)
