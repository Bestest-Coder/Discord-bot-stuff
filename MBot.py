import discord
from discord.ext.commands import Bot
from discord.ext import commands
import time
import asyncio
import random
import os
import env
import base64
import requests

Client = discord.Client()
client = commands.Bot(command_prefix='=')
client.commanderids = [357596253472948224, os.environ["SILI-ID"]]
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
    icn = guild.icon_url
    if guild.icon_url == '':
        icn = "no icon"
    await client.get_user(357596253472948224).send('''M'Bot was added to: {}
Owned by: {}
ID: {}
Icon: {}'''.format(guild.name, guild.owner.name, guild.id, icn))
    payload = {"server_count" : len(client.guilds)}
    r = requests.post('https://botsfordiscord.com/api/bot/429781887486001163', headers={"Content-Type" : "application/json", "Authorization" : env.gettoken(2)}, json=payload)
    await client.get_user(357596253472948224).send(str(r))

@client.event
async def on_guild_remove(guild):
    await client.get_user(357596253472948224).send('''M'Bot was removed from: {}
Owned by: {}'''.format(guild.name, guild.owner.name))
    payload = {"server_count" : len(client.guilds)}
    r = requests.post('https://botsfordiscord.com/api/bot/429781887486001163', headers={"Content-Type" : "application/json", "Authorization" : env.gettoken(2)}, json=payload)
    await client.get_user(357596253472948224).send(str(r))

if __name__ == '__main__':
    for extension in startup_extensions:
        try:
            client.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))
client.run(env.tokenget(1))

'''
___________________6666666___________________
____________66666__________66666_____________
_________6666___________________666__________
_______666__6____________________6_666_______
_____666_____66_______________666____66______
____66_______66666_________66666______666____
___66_________6___66_____66___66_______666___
__66__________66____6666_____66_________666__
_666___________66__666_66___66___________66__
_66____________6666_______6666___________666_
_66___________6666_________6666__________666_
_66________666_________________666_______666_
_66_____666______66_______66______666____666_
_666__666666666666666666666666666666666__66__
__66_______________6____66______________666__
___66______________66___66_____________666___
____66______________6__66_____________666____
_______666___________666___________666_______
_________6666_________6_________666__________
____________66666_____6____66666_____________
___________________6666666___________________
'''
