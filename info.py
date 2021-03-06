import discord
from discord.ext import commands

class Information(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(brief='Gets the invite link for the bot')
    async def invite(self, ctx):
        perms = discord.Permissions.none() #autogenerate bot link with proper permissions
        perms.read_messages = True
        perms.send_messages = True #better safe then sorry
        perms.manage_messages = True
        perms.embed_links = True
        perms.read_message_history = True
        perms.attach_files = True
        app_info = await self.client.application_info()
        await ctx.send("Here's the invite for the bot\n{0}".format(discord.utils.oauth_url(app_info.id, perms)))

    @commands.command(brief='tells you who made the bot')
    async def contributors(self, ctx):
        await ctx.channel.send("""The Bestest User#6969: The original creator. GitHub: https://github.com/Bestest-Coder
siliconwolf#0013: Cool man who helped make a lot of stuff work, and contributed his site to store data. GitHub: https://github.com/silicWulf""")

    @commands.command(brief='all the basic info about the bot')
    async def info(self, ctx):
        await ctx.channel.send("This bot was first created November 20th 2017, and has gone through several name iterations.\nFor details, help, or to offer support visit Bots for Discord at https://botsfordiscord.com/bot/429781887486001163")

    @commands.command(brief='gives you the link to the development/testing server')
    async def server(self, ctx):
        await ctx.channel.send("Questions, comments, or suggestions? Come see the testing server at https://discord.gg/gCvAYtu")

def setup(client):
    client.add_cog(Information(client))
