import discord
from discord.ext import commands
import env
import re


CLINK_NAME = "clink"
try:
    # CLINK_CHAR_LIMIT = await env.get("clink-char-limit")
    CLINK_CHAR_LIMIT = 300   # aHHHH figure out a way to get the abiove to woi tirjk
except ValueError:
    CLINK_CHAR_LIMIT = 300
    # await env.set("clink-char-limit", 300)
except env.GetReturnedNothing:
    CLINK_CHAR_LIMIT = 300
    # await env.set("clink-char-limit", 300)
user = discord.Member
safe = discord.Object


async def get_clink_toggle(sid):
    try:
        ct = await env.get(str(sid) + "-clink_toggle")
        if ct == "variable does not exist":
            raise TypeError("")
        ct = bool(int(ct))
    except TypeError:
        await env.set(str(sid) + "-clink_toggle", "1")
        ct = True
    return ct


class on_msg(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        global CLINK_CHAR_LIMIT
        CLINK_CHAR_LIMIT = await env.get("clink-char-limit")
        CLINK_CHAR_LIMIT = int(CLINK_CHAR_LIMIT)

    @commands.Cog.listener()
    async def on_message(self, message):
        global CLINK_CHAR_LIMIT
        if message.content == "" and len(message.attachments) == 0:  # if for some reason the content is empty, possibly a pin?
            return

        if message.author == self.client.user:
            return  # we do not want the bot to reply to itself

        if message.author.bot is True:  # disallow bots from getting responses
            return

        try:
            message.channel.name
        except AttributeError:  # probably a dm
            pass
        else:
            if message.channel.name == CLINK_NAME:  # for now, let's have all bots be able to send their messages through
                CLINK_CHAR_LIMIT = await env.get("clink-char-limit")
                CLINK_CHAR_LIMIT = int(CLINK_CHAR_LIMIT)
                if len(message.content) >= CLINK_CHAR_LIMIT:
                    await message.author.send(f"Your Clink message was too long. Messages must be lower than {CLINK_CHAR_LIMIT} characters in length.")
                    return
                if message.content.count('\n') >= 2:
                    try:
                        await message.author.send("Your Clink message was too long. Messages must have less than 3 new lines")
                        return
                    except discord.Forbidden:
                        await message.channel.send("{}, your Clink message was too long. Messages must have less than 3 new lines".format(message.author.mention))
                        return
                if message.content == '_ _':
                    try:
                        await message.author.send("Your Clink message cannot appear to be empty")
                        return
                    except discord.Forbidden:
                        await message.channel.send("{}, your Clink message cannot appear to be empty".format(message.author.mention))
                        return
                blockwords = await env.get("clink-blockedwords")
                blockwords = blockwords.split("\x00")
                for word in blockwords:
                    if word in message.content:
                        return
                banlist = await env.get("clink-banlist")
                banlist = banlist.split("\x00")
                is_banned = False
                for ban in banlist:
                    if str(message.author.id) == ban:
                        is_banned = True
                if not is_banned:
                    this_clink_toggle = await get_clink_toggle(message.guild.id)
                    if this_clink_toggle:  # if they want to send messages
                        for guild in self.client.guilds:  # for each server
                            x = await get_clink_toggle(guild.id)
                            if x:  # if this server wants to get messages
                                for channel in guild.channels:  # send
                                    if channel.id != message.channel.id:
                                        if channel.name == CLINK_NAME:  # the
                                            msg = message.content
                                            urls = re.findall("https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+", msg)
                                            for url in urls:
                                                msg = msg.replace(url, f"<{url}>")  # remove all url embeds
                                            for mention in message.mentions:
                                                msg = msg.replace(mention.mention, f"(at){mention.name}".replace("@", "(at)"))  # removes all mentions
                                            msg = msg.replace("@", "(at)")  # gets rid of @here and @everyone
                                            att = [f"<{a.url}>" for a in message.attachments]
                                            att = " ".join(att)
                                            try:
                                                await channel.send(f"({message.guild.name}) {message.author.name} - {msg} {att}")  # message
                                            except AttributeError:  # definitely happens on CategoryChannel, which for some reason gets detected?
                                                pass  # ignore
                                            except discord.Forbidden:
                                                pass  # ignore inability to send message to channel
        for i in range(len(message.mentions)):
            if message.mentions[i] == self.client.user:
                await message.channel.send('use = next time you want to talk moron'.format(message))

        for i in range(len(message.mentions)):
            if await env.get("{}_isafk".format(message.mentions[i].id)) == "True":
                await message.channel.send(":speaker: {}, {} is afk because: {}".format(message.author.mention,message.mentions[i].name,await env.get("{}_afkmsg".format(message.mentions[i].id)))) #current record for longest line in the code at 196

        if await env.get("{}_isafk".format(message.author.id)) == "True" and not message.content.startswith("=afk"):
            await env.set("{}_isafk".format(message.author.id), False)
            await message.channel.send("{} is no longer AFK".format(message.author.mention))
'''
    async def on_reaction_add(self,react,user):
        if react.emoji == ":stuffed_flatbread:":
            if react.count == 10:
                bith = await env.get(f"{react.message.guild.id}-react_channel")
                if bith == 'variable does not exist':
                    await react.message.channel.send("There is no set channel for breadpins")
                else:
                    em = discord.Embed()
                    em.set_author(react.message.author.name,icon_url=react.message.author.avatar_url)
                    em.description = react.message.content
                    ech = await env.get(f"{react.message.guild.id}-react_channel")
                    await discord.utils.get(self.client.get_all_channels(), id=ech).send(embed=em)
                    ''' #breadpin original code, probably has some issues but no plans to fix

def setup(client):
    client.add_cog(on_msg(client))
