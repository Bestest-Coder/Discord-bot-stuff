import random
import discord
from discord.ext import commands


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
    async def pfp(self, ctx, *, user: discord.User):
        em = discord.Embed()
        em.set_image(url=user.avatar_url_as(None,'png'))
        await ctx.channel.send(embed=em)

    @commands.command()
    async def void(self, ctx):
        await ctx.channel.send('_ _')


def setup(client):
    client.add_cog(General(client))
