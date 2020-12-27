import re
import env
import random
import discord
import role_checks
from discord.ext import commands
import pysaucenao
import hashlib


MAX_TAG_LEN = 300

def embedAvatarDetails(self, daUser, daEmbed):
    if not daEmbed.image.width == discord.Embed.Empty:
        daEmbed.set_footer(text=str(daEmbed.image.width)+"x"+str(daEmbed.image.height)) #'{}x{}'.format(daEmbed.image.width,daEmbed.image.height))
    daEmbed.set_author(name="{}#{}".format(daUser.name,daUser.discriminator), url=daUser.avatar_url_as(static_format='png'))
    daEmbed.color = discord.Color.from_rgb(random.randint(0,255),random.randint(0,255),random.randint(0,255))
    return daEmbed

class General(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.sauce = pysaucenao.SauceNao(api_key=env.tokenget(2))
        self.eightBallResponses = ['It is certain', 'Without a doubt', 'You may rely on it', 'Yes definitely', 'It is decidedly so',
                  'As I see it, yes', 'Most likely', 'Yes', 'Outlook good', 'Signs point to yes', 'Reply hazy try again',
                  'Better not tell you now', 'Ask again later', 'Cannot predict now', 'Concentrate and ask again',
                  "Don't count on it", 'Outlook not so good', 'My sources say no', 'Very doubtful', 'My reply is no']

    @commands.command(name='8ball')
    async def balls(self, ctx, *, question):
        questionbytes = bytes(question, 'utf-8')
        slinger = hashlib.md5()
        slinger.update(questionbytes)
        answer = self.eightBallResponses[(int(slinger.hexdigest(), 16)) % 19]
        daMessage = f"> {question}\n{answer}"
        await ctx.send(daMessage)

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
    async def random_(self, ctx, num1: int, num2: int): #could probably fix naming, but it works
        await ctx.channel.send(str(random.randint(num1, num2)))

    @commands.command(brief="get's the users avatar/pfp, by default returns your own")
    async def pfp(self, ctx, *, user=None):
        try:
            em = discord.Embed() #issues arise when just using straight URL so embeds work beetter
            if user is not None:
                try:
                    targetUser = await commands.UserConverter().convert(ctx, user)
                except commands.errors.BadArgument:
                    try:
                        targetUser = await self.client.fetch_user(int(user))
                    except discord.NotFound:
                        await ctx.send("Error: no user found with ID")
                        return
                    except ValueError:
                        await ctx.send("Error: Invalid input, possible server issue try again in a few minutes")
                        return
                em.set_image(url=targetUser.avatar_url_as(static_format='png'))
                em = embedAvatarDetails(self,targetUser, em)
            else:
                em.set_image(url=ctx.message.author.avatar_url_as(static_format='png')) #in case some specifics don't work
                em = embedAvatarDetails(self,ctx.message.author,em)
            await ctx.channel.send(embed=em)
        except discord.errors.Forbidden:
            await ctx.channel.send("Error: cannot send embeds")

    @commands.command()
    async def void(self, ctx):
        await ctx.channel.send('_ _')

    @commands.command(brief='show your tag')
    async def tag(self, ctx):
        usertag = await env.get('{}_tag_{}'.format(ctx.message.guild.id, ctx.message.author.id)) #gets tag from the pickle database
        if usertag == 'variable does not exist':
            await ctx.channel.send("You don't have a tag. Set a tag with `=settag <text>`")
        else:
            await ctx.channel.send('📎 ' + usertag) #use a file emote to prevent bot commands from being used

    @commands.command(brief='set your own tag')
    async def settag(self, ctx):
        content = ctx.message.content
        tag = ' '.join(ctx.message.content.split(' ')[1:])  # get everything that isn't the first section
        aurls = [a.url for a in ctx.message.attachments]
        tag += ' ' + ' '.join(aurls)
        links = re.findall("(https?://[^\s]+)", tag)
        if len(tag) == 0: #elif stack to remove problematic tags
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
            await env.set("{}_tag_{}".format(ctx.message.guild.id, ctx.message.author.id), tag) #tags are stored in pickle database using format guildid_tag_userid
            await ctx.channel.send("<@{}>, your tag has been set.".format(ctx.message.author.id))

    @commands.command(brief='WHAT. WHAT THE FUCK -Jontron')
    async def wtf(self,ctx):
        await ctx.channel.send(file=discord.File('wtf.mp4', filename='wtf.mp4'))

    @commands.command(brief='No. NOOOOOOOO -Lion Moses')
    async def no(self,ctx):
        await ctx.channel.send(file=discord.File('no.mp4', filename='no.mp4'))

    @commands.command(brief="Sets you to AFK")
    async def afk(self,ctx):
        if await env.get("{}_afkmsg".format(ctx.message.author.id)) == 'variable does not exist': #prevent AFK with no message, might add default message in future
            await ctx.channel.send("You have no AFK message, set one before continuing")
        else:
            await env.set("{}_isafk".format(ctx.message.author.id),True) #afk status is defined only by userid as it's cross-server
            await ctx.channel.send("You are now AFK")

    @commands.command(brief="sets your afk response message")
    async def afkmsgset(self, ctx, *, content: str):
        if ctx.message.mentions != []: #elif stacks to check for unwanted stuff again
            await ctx.channel.send("You cannot mention people in your afk message")
        elif "@everyone" in content or "@here" in content:
            await ctx.channel.send("You cannot mass ping in your afk message")
        elif len(content) > 50:
            await ctx.channel.send("Your message is too long")
        else:
            await env.set("{}_afkmsg".format(ctx.message.author.id),content)
            await ctx.channel.send("Your AFK message is now: {}".format(content))

    @commands.command(brief="Uses the SauceNao API to find the sources of images", aliases=["saucethis"])
    async def sourcethis(self,ctx, *, givenURL=None):
        if givenURL is None:
            if len(ctx.message.attachments) != 0:
                targetUrl = ctx.message.attachments[0].url
            else:
                await ctx.send("No attachment or URL provided")
                return
        else:
            targetUrl = givenURL
        async with ctx.typing():
            try:
                results = await self.sauce.from_url(targetUrl)
            except pysaucenao.errors.DailyLimitReachedException:
                await ctx.send("Error: Daily limit reached, try again later")
                return
            except pysaucenao.errors.ShortLimitReachedException:
                await ctx.send("Error: 30 second limit reached, try again in a minute")
                return
            if len(results) == 0:
                await ctx.send("No source found, website may have better results")
                return
            daEmbed = discord.Embed()
            daEmbed.title = ("Title: "+results[0].title if results[0].title is not None else 'Title not found')
            daEmbed.url = results[0].url
            if results[0].author_name is not None:
                daEmbed.set_author(name="Author: " + results[0].author_name,
                                   url=results[0].author_url if results[0].author_url is not None else results[0].url)
            footerText = f'Similarity: {str(results[0].similarity)}% | Remaining requests: {results.long_remaining}'
            daEmbed.set_footer(text=footerText)
            daEmbed.set_thumbnail(url=results[0].thumbnail)
            if len(results) >= 2:
                daEmbed.add_field(name="Alternate Sources", value="Primary source is linked in title and author fields",
                                  inline=False)
                for result in results[1:]:
                    daEmbed.add_field(name=result.title, value=result.url, inline=True)
            await ctx.send(embed=daEmbed)

def setup(client):
    client.add_cog(General(client))
