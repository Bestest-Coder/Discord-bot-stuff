import discord
from discord.ext.commands import Bot
from discord.ext import commands
import time
import asyncio
import random
import os
import env
import base64

Client = discord.Client()
client = commands.Bot(command_prefix='=')
client.commanderids = [os.environ["ME-ID"], os.environ["SILI-ID"]]
client.commanderids = list(client.commanderids)
user = discord.Member
startup_extensions = ['moderation', 'general', 'on_message_stuff', 'info']
client.data = {'test': 'test object'}


async def stafforcomm(self, inp):
    if '[no]' not in inp.author.display_name:
        if ifcomm(self, inp):
            return True

    sst = await env.get('{}_stfrole'.format(str(inp.guild.id)))
    try:
        if sst == 'variable does not exist':  # if var error from server
            return False  # since there is no mod role to compare against anyways
        server_stfrole = int(sst)
    except ValueError:
        raise ValueError(f'server_stfrole can\'t be assigned to {sst}, probably not a real id. maybe define a staffrole with an id?')
    if server_stfrole == discord.utils.get(inp.author.roles, id=server_stfrole).id:  # check to make sure the ids are the same
        return True
    else:
        return False


def ifcomm(inp):
    if inp.author.id in client.commanderids:
        return True
    else:
        return False


@client.command(brief="Comm Only: sets the bot's name", hidden=True)
async def botname(ctx, *, botname: str):
    if not ifcomm(ctx.message):
        return
    await client.user.edit(username=botname)
    msg = 'Username has now been set to ' + botname
    await ctx.channel.send(msg)
    print((str(ctx.author) + ': ') + msg)


@client.command(hidden=True)
async def play(ctx, *, gamename: str):
    if not ifcomm(ctx.message):
        return
    game = discord.Game(gamename)
    await client.change_presence(activity=game)
    await env.set('GAME_NAME', gamename)
    await ctx.channel.send("I'm now playing: " + gamename)

@client.command(hidden=True)
async def debug(ctx):
    if not ifcomm(ctx.message):
        return
    try:
        envs = os.environ.copy()
        try:
            del envs[os.environ['BOTTOKEN']]  # remove bot token from debug for security
        except KeyError:  # please god don't post the token
            await ctx.channel.send("no please don't")
            return  # end me
        # await ctx.message.author.send(str(envs))
        user = client.get_user(ctx.message.author.id)  # i'm really at a i || || |_
        await user.send(str(envs))
    except Exception as e:  # in case of any problems
        simple_traceback = e.__class__.__name__ + ': ' + e.args[0]
        await ctx.channel.send(simple_traceback)

'''
@client.event
async def on_message_edit(before, after):
    if before.author.bot is True:
        return
    fmt = '**{0.author}** edited their message from "{1.content}" to "{0.content}"'
    print(fmt.format(after, before))
'''

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('Build: debug 5')
    print('------')
    get_game = await env.get('GAME_NAME')
    if type(get_game) == str and get_game != '':
        game = discord.Game(await env.get('GAME_NAME'))
    else:
        game = discord.Game("with katana")
    await client.change_presence(activity=game)

@client.event
async def on_guild_join(guild):
    await client.get_user(357596253472948224).dm_channel.send(''''M'Bot was added to: {}
    Owned by: {}
    ID: {}
    Icon: {}'''.format(guild.name,guild.owner.name,guild.id,guild.icon_url))

if __name__ == '__main__':
    for extension in startup_extensions:
        try:
            client.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))
client.run(os.environ['BOTTOKEN'])
