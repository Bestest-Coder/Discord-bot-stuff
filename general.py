import re
import env
import random
import discord
import role_checks
from discord.ext import commands


MAX_TAG_LEN = 300
auth = ctx.message.author

class General():
    def __init__(self, client):
        self.client = client

    @commands.command(brief='sends the "Several people are typing" gif')
    async def sevpeople(self, ctx):
        await ctx.channel.send(
            file=discord.File('several people are typing.gif', filename='several people are typing.gif'))
        await ctx.message.delete()

    @commands.command(brief='A nice gif of dancing kirby')
    async def dancing(self, ctx):
        await ctx.channel.send(file=discord.File('kirby dance.gif', filename='kirby dance.gif'))
        await ctx.message.delete()

    @commands.command(brief='sends the USSR symbol')
    async def communism(self, ctx):
        await ctx.channel.send('☭')
        await ctx.message.delete()

    @commands.command(brief='generates a random number between the two given numbers', name='random')
    async def random_(self, ctx, num1: int, num2: int):
        await ctx.channel.send(str(random.randint(num1, num2)))

    @commands.command(brief="get's the users avatar/pfp")
    async def pfp(self, ctx, *, user=auth):
        try:
            em = discord.Embed()
            em.set_image(url=user.avatar_url_as(static_format='png'))
            await ctx.channel.send(embed=em)
        except discord.errors.Forbidden:
            await ctx.channel.send("Error: cannot send embeds")

    @commands.command()
    async def void(self, ctx):
        await ctx.channel.send('_ _')

    @commands.command(brief='show your tag')
    async def tag(self, ctx):
        usertag = await env.get('{}_tag_{}'.format(ctx.message.guild.id, ctx.message.author.id))
        if usertag == 'variable does not exist':
            await ctx.channel.send("You don't have a tag. Set a tag with `=settag <text>`")
        else:
            await ctx.channel.send('📎 ' + usertag)

    @commands.command(brief='set your own tag')
    async def settag(self, ctx):
        content = ctx.message.content
        tag = ' '.join(ctx.message.content.split(' ')[1:])  # get everything that isn't the first section
        aurls = [a.url for a in ctx.message.attachments]
        tag += ' ' + ' '.join(aurls)
        links = re.findall("(https?://[^\s]+)", tag)
        if len(tag) == 0:
            await ctx.channel.send("Error: your tag is empty, will not store.")
        elif len(tag) >= MAX_TAG_LEN:
            await ctx.channel.send("Error: your tag is above {} characters, will not store.".format(MAX_TAG_LEN))
        elif len(links) > 1:
            await ctx.channel.send("Error: your tag has more than one link and/or attachment, will not store.")
        elif len(ctx.message.mentions) != 0:
            await ctx.channel.send("Error: your tag has one or more mentions.")
        elif "@everyone" in content or "@here" in content:
            await ctx.channel.send("Error: your message contains a mass ping")
        else:
            await env.set("{}_tag_{}".format(ctx.message.guild.id, ctx.message.author.id), tag)
            await ctx.channel.send("<@{}>, your tag has been set.".format(ctx.message.author.id))

    @commands.command(brief='WHAT. WHAT THE FUCK -Jontron')
    async def wtf(self,ctx):
        await ctx.channel.send(file=discord.File('wtf.mp4', filename='wtf.mp4'))

    @commands.command(brief='No. NOOOOOOOO -Lion Moses')
    async def no(self,ctx):
        await ctx.channel.send(file=discord.File('no.mp4', filename='no.mp4'))

    @commands.command(brief="Sets you to AFK")
    async def afk(self,ctx):
        if await env.get("{}_afkmsg".format(ctx.message.author.id)) == 'variable does not exist':
            await ctx.channel.send("You have no AFK message, set one before continuing")
        else:
            await env.set("{}_isafk".format(ctx.message.author.id),True)
            await ctx.channel.send("You are now AFK")

    @commands.command(brief="sets your afk response message")
    async def afkmsgset(self, ctx, *, content: str):
        if ctx.message.mentions != []:
            await ctx.channel.send("You cannot mention people in your afk message")
        elif "@everyone" in content or "@here" in content:
            await ctx.channel.send("You cannot mass ping in your afk message")
        else:
            await env.set("{}_afkmsg".format(ctx.message.author.id),content)
            await ctx.channel.send("Your AFK message is now: {}".format(content))


def setup(client):
    client.add_cog(General(client))
