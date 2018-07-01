import discord
from discord.ext import commands

class Information():
    def __init__(self, client):
        self.client = client

    @commands.command(brief='Gets the invite link for the bot')
    async def invite(self, ctx):
        perms = discord.Permissions.none()
        perms.read_messages = True
        perms.send_messages = True
        perms.manage_messages = True
        perms.embed_links = True
        perms.read_message_history = True
        perms.attach_files = True
        app_info = await self.client.application_info()
        await ctx.send("Here's the invite for the bot\n{0}".format(discord.utils.oauth_url(app_info.id, perms)))

    @commands.command(brief='tells you who made the bot')
    async def contributors(self, ctx):
        await ctx.channel.send('''
        The Bestest User#6969: The original creator. GitHub: https://github.com/Bestest-Coder
        siliconwolf#0013: Cool man who helped make a lot of stuff work, and contributed his site to store data. GitHub: https://github.com/silicWulf''')

    @commands.command(brief='all the basic info about the bot')
    async def info(self, ctx):
        await ctx.channel.send("This bot was first created November 20th 2017, and has gone through several name iterations. It is hosted on Heroku and can be found on GitHub at https://github.com/Bestest-Coder/Discord-bot-stuff.")

    @commands.command(brief='gives you the link to the development/testing server')
    async def server(self, ctx):
        await ctx.channel.send("Come see the testing server: https://discord.gg/EkAZfk9")

def setup(client):
    client.add_cog(Information(client))
