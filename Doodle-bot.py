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
client.commanderids = [357596253472948224, 227598467621584908]
client.commanderids = list(client.commanderids)
user = discord.Member
startup_extensions = ['moderation', 'general', 'on_message_stuff']
client.data = {'test': 'test object'}


def stafforcomm(inp):
    if ifcomm(inp):  # less redundant
        return True
    # if client.data[str(inp.guild)]['stfrole'] == discord.utils.get(inp.author.roles, id=self.client.staffrole.id):
    if int(env.get('{}.stfrole'.format(inp.guild.id))) in [role.id for role in inp.author.roles]:  # more efficient, gets all role ids
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
    env.set('GAME_NAME', gamename)
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
    print('------')
    try:
        game = discord.Game(env.get('GAME_NAME'))
    except KeyError:
        game = discord.Game("with katana")
    await client.change_presence(activity=game)


if __name__ == '__main__':
    for extension in startup_extensions:
        try:
            client.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))
client.run(env.get('BOTTOKEN'))
