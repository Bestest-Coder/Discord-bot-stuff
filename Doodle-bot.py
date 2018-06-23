import discord
from discord.ext.commands import Bot
from discord.ext import commands
import time
import asyncio
import random
import os
import env

Client = discord.Client()
client = commands.Bot(command_prefix='=')
client.commanderid = 357596253472948224
user = discord.Member
startup_extensions = ['moderation', 'general', 'on_message_stuff']
client.data = {'test': 'test object'}


def stafforcomm(inp):
    if client.commanderid == inp.author.id:
        return True
    # if client.data[str(inp.guild)]['stfrole'] == discord.utils.get(inp.author.roles, id=self.client.staffrole.id):
    if int(env.get('{}.stfrole'.format(inp.guild.id))) in [role.id for role in inp.author.roles]:  # more efficient, gets all role ids
        return True
    else:
        return False


def ifcomm(inp):
    if client.commanderid == inp.author.id:
        return True
    else:
        return False


@client.command(brief="Comm Only: sets the bot's name", hidden=True)
async def botname(ctx, *, botname: str):
    if ifcomm(ctx.message) is False:
        return
    await client.user.edit(username=botname)
    msg = 'Username has now been set to ' + botname
    await ctx.channel.send(msg)
    print((str(ctx.author) + ': ') + msg)


@client.command(hidden=True)
async def play(ctx, *, gamename: str):
    if ifcomm(ctx.message) is False:
        return
    game = discord.Game(gamename)
    await client.change_presence(activity=game)
    env.set('GAME_NAME', gamename)
    await ctx.channel.send("I'm now playing: " + gamename)


@client.event
async def on_message_edit(before, after):
    if before.author.bot is True:
        return
    fmt = '**{0.author}** edited their message from "{1.content}" to "{0.content}"'
    print(fmt.format(after, before))


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
client.run(os.environ['BOTTOKEN'])
