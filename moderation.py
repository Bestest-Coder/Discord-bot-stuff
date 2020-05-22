import discord
from discord.ext import commands
import asyncio
import env
import re
import role_checks
import requests
user = discord.Member
DEBUG = True


MAX_TAG_LEN = 300


async def stafforcomm(self, inp):
    #if '[no]' not in inp.author.display_name:
        #if ifcomm(self, inp):
            #return True
    if ifcomm(self, inp):
        return True
    sst = await env.get('{}_stfrole'.format(str(inp.guild.id)))
    try:
        if sst == 'variable does not exist':  # if var error from server
            return False  # since there is no mod role to compare against anyways
        server_stfrole = int(sst)
    except ValueError:
        raise ValueError(f'server_stfrole can\'t be assigned to {sst}, probably not a real id. maybe define a staffrole with an id?')
    try:
        if server_stfrole == discord.utils.get(inp.author.roles, id=server_stfrole).id:  # check to make sure the ids are the same
            return True
        else:
            return False
    except AttributeError:  # if .id not on None
        return False  # they don't have the required role


def ifcomm(self, inp):
    if inp.author.id in self.client.commanderids:
        return True
        print("is yes")
    else:
        return False
        print("is no")


def ifvip(self, inp):
    if inp.author.id in self.client.commanderids:
        return True
    if inp.guild.owner == inp.author:
        return True
    if inp.author.guild_permissions.administrator is True:
        return True
    else:
        return False


class Staff(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(brief='sends a message to warning channel')
    async def warn(self, ctx, war_user: user, *, reason: str):
        if await stafforcomm(self, ctx.message) is False:
            print(str(ctx.author) + " tried to warn but isn't staff")
            return
        #com_send = ctx.author
        if reason is None:
            reason = ''
        msg = (war_user.mention + ', you have recieved a warning for '
               ) + reason  #  + ', this is warning #' + str(war_user.warns) + 'at the hands of ' + str(com_send)
        wchan_id = int(await env.get('{}_wchan'.format(str(ctx.message.guild.id))))
        wchan = discord.utils.get(self.client.get_all_channels(), id=wchan_id)  # get real channel behind the id
        await wchan.send(msg)
        #print((((str(ctx.author) + ': ') + str(war_user)) + ' has been warned for: ') + reason)

    @commands.command(brief="set's the warning channel")
    async def wchan(self, ctx, wchan: discord.TextChannel):
        if ifcomm(self, ctx.message) is False:
            return
        # self.client.data[str(ctx.message.guild.id)]['wchan'] = wchan.id
        to_set = '{}_wchan'.format(str(ctx.message.guild.id))
        await env.set(to_set, wchan.id)  # set the wchan id with var name guildid_wchan
        msg = 'Warning channel is ' + str(wchan)
        await ctx.channel.send(msg)
        #print((str(ctx.author) + ': ') + msg)

    @commands.command(brief='makes the bot say the content')
    async def say(self, ctx, *, content: str):
        if ifcomm(self, ctx.message) is False:
            return
        await ctx.channel.send(content.format(ctx.message))
        try:
            await ctx.message.delete()
        except discord.ext.commands.errors.CommandInvokeError:
            print('could not delete message (commandinvokeerror) (id: {}) in say'.format(ctx.message.id))
        except discord.errors.Forbidden:
            print('could not delete message (permissions) (id: {}) in say'.format(ctx.message.id))
        #print(((str(ctx.author) + ': ') + 'Bot said : ') + content)

    @commands.command(brief='say but less suspiscous')
    async def dsay(self, ctx, *, content: str):
        result = await stafforcomm(self, ctx.message)
        if result is not True:
            return
        #sfc = await stafforcomm(self, ctx.message)
        #print(stafforcomm)
        #print(sfc)
        #if sfc is not True:
            #print(f'stafforcomm returned false with id {ctx.message.id}')
            #return
        #print('either stafforcomm returned true or python is being stupid')
        dest = ctx.channel
        dur = len(ctx.message.content) * 0.1
        try:
            await ctx.message.delete()
        except discord.ext.commands.errors.CommandInvokeError:
            print('could not delete message (id: {}) in dsay'.format(ctx.message.id))
        except discord.errors.Forbidden:
            print('could not delete message (id: {}) in dsay'.format(ctx.message.id))
        await dest.trigger_typing()
        await asyncio.sleep(dur)
        await dest.send(content)

    @commands.command(brief='sets the staff role')
    async def staffrole(self, ctx, *, staffrole: discord.Role):
        if ifvip(self, ctx.message) is False:
            return
        #if str(ctx.message.guild) in self.client.data == False:
            #self.client.data[str(ctx.message.guild.id)]
        # self.client.data[str(ctx.message.guild.id)] = {'stfrole': staffrole}
        await env.set('{}_stfrole'.format(str(ctx.message.guild.id)), staffrole.id)  # set guildid_stfrole to the given staffrole's id
        msg = 'staff role has been set to ' + str(staffrole)
        await ctx.channel.send(msg)
        #print((str(ctx.author) + ': ') + msg)

    @commands.command(brief="Sets the bot's nickname")
    async def nick(self, ctx, *, name: str):
        if await stafforcomm(self, ctx.message) is False:
            return
        await ctx.message.guild.me.edit(nick=name)
        await ctx.channel.send('Nickname is now "' + name + '"')

    @commands.command(brief="toggle cross-server chat (clink)")
    async def toggleclink(self, ctx):
        # is_sfc = await role_checks.stafforcomm(self, msg)
        msg = ctx.message
        is_sfc = await stafforcomm(self, msg)
        if is_sfc:
            ct = f"{msg.guild.id}-clink_toggle"
            x = await env.get(ct)
            x = not int(x)
            await env.set(ct, int(x))
            print("debug", ct, int(x))
            await ctx.channel.send(f"Toggled. Clink on: {'yes' if x else 'no'}")

    @commands.command(brief="list all servers/ids with this bot")
    async def guildlist(self, ctx):
        # is_comm = await role_checks.ifcomm(self, ctx)
        is_comm = ifcomm(self, ctx)
        if is_comm:
            await ctx.author.send("\n".join([f"{g.name} ({g.id})" for g in self.client.guilds]))
            await ctx.author.send(str(len(self.client.guilds)))
            payload = {"server_count" : len(self.client.guilds)}
            r = requests.post('https://botsfordiscord.com/api/bot/429781887486001163', headers={"Content-Type" : "application/json", "Authorization" : env.tokenget(1)}, json=payload)
            await self.client.get_user(357596253472948224).send(str(r))

    @commands.command(brief="toggle another server's clink")
    async def toggleguildclink(self, ctx):
        # is_comm = await role_check.ifcomm(self, ctx)
        is_comm = ifcomm(self, ctx)
        if is_comm:
            arg = ctx.message.content.split(" ")
            if len(arg) != 2:
                await ctx.channel.send("Incorrect syntax. Syntax: `=toggleguildclink <guild id or name>`")
            try:
                gid = int(arg[1])
                gcount = [g.id for g in self.client.guilds].count(gid)
                if gcount == 0:
                    await ctx.channel.send(f"Server ID {gid} not found in bot server list.")
                    return
                elif gcount > 1:
                    await ctx.channel.send("More than one server has this ID. If this happens, something is wrong with the bot.")
                    return
                x = await env.get(f"{gid}-clink_toggle")
                await env.set(f"{gid}-clink_toggle", int(not x))
                await ctx.channel.send(f"Set server ID (or maybe name) Clink toggle to {bool(gid)}")
            except ValueError:  # not only numbers, probably in the first line int()
                c = self.client.guilds.count(arg[1])
                if c != 1:
                    await ctx.channel.send("There is more than one server with that name. Use the command =guildlist to find the desired server ID.")
                    return
                for guild in self.client.guilds:
                    if guild.name == arg[1]:
                        x = await env.get(f"{gid}-clink_toggle")
                        await env.set(f"{gid}-clink_toggle", int(not x))
                        await ctx.channel.send(f"Set server name Clink toggle to {bool(gid)}")

    @commands.command(brief="alter the clink char limit")
    async def clinkmaxchars(self, ctx):
        is_comm = ifcomm(self, ctx)
        if is_comm:
            sp = ctx.message.content.split(" ")
            if len(sp) != 2:
                await ctx.channel.send("Incorrect syntax. Syntax: `=clinkmaxchars <max char number>`")
                return
            arg = sp[1]
            try:
                arg = int(arg)
            except ValueError:
                await ctx.channel.send("That's not a number.")
                return
            await env.set("clink-char-limit", arg)
            await ctx.channel.send("CLINK_MAX_CHARS/clink-max-chars set.")

    @commands.command(brief="ban a word from clink")
    async def clinkwordban(self, ctx):
        is_comm = ifcomm(self, ctx)
        if is_comm:
            sp = ctx.message.content.split(" ")
            if len(sp) != 2:
                await ctx.channel.send("Incorrect syntax. Syntax: `=clinkwordban <word>`")
                return
            arg = sp[1]
            banlist = await env.get("clink-blockedwords")
            banlist = set(banlist.split("\x00"))
            banlist.add(arg)
            banlist = "\x00".join(banlist)
            await env.set("clink-blockedwords", banlist)
            await ctx.channel.send(f"Word '{arg}' banned.")

    @commands.command(brief="unban a word from clink")
    async def clinkwordunban(self, ctx):
        is_comm = ifcomm(self, ctx)
        if is_comm:
            sp = ctx.message.content.split(" ")
            if len(sp) != 2:
                await ctx.channel.send("Incorrect syntax. Syntax: `=clinkwordunban <word>`")
                return
            arg = sp[1]
            banlist = await env.get("clink-blockedwords")
            banlist = set(banlist.split("\x00"))
            banlist.remove(arg)
            banlist = "\x00".join(banlist)
            await env.set("clink-blockedwords", banlist)
            await ctx.channel.send(f"Word '{arg}' unbanned.")

    @commands.command(brief="ban a user from clink")
    async def clinkban(self, ctx):
        is_comm = ifcomm(self, ctx)
        if is_comm:
            sp = ctx.message.content.split(" ")
            if len(sp) != 2:
                await ctx.channel.send("Incorrect syntax. Syntax: `=clinkban <id or full username>`")
                return
            arg = sp[1]
            member = None
            for guild in self.client.guilds:
                for mem in guild.members:
                    if str(mem.id) == arg or str(mem) == arg:  # if mem.id == given id or smth yeah
                        banlist = await env.get("clink-banlist")
                        banlist = banlist.split("\x00")
                        if str(mem.id) not in banlist:
                            banlist.append(str(mem.id))
                        else:
                            await ctx.channel.send("Ban already given to user!")
                            return
                        await env.set("clink-banlist", "\x00".join(banlist))
                        await ctx.channel.send(f"Ban given to {str(mem)}.")
                        return
            await ctx.channel.send("User not found with given ID or username.")

    @commands.command(brief="unban a user from clink")
    async def clinkunban(self, ctx):
        is_comm = ifcomm(self, ctx)
        if is_comm:
            sp = ctx.message.content.split(" ")
            if len(sp) != 2:
                await ctx.channel.send("Incorrect syntax. Syntax: `=clinkban <id or full username>`")
                return
            arg = ctx.message.content.split(" ")[1]
            member = None
            for guild in self.client.guilds:
                for mem in guild.members:
                    if str(mem.id) == arg or str(mem) == arg:  # if mem.id == given id or smth yeah
                        banlist = await evn.get("clink-banlist")
                        banlist = banlist.split("\x00")
                        if str(mem.id) not in banlist:
                            await ctx.channel.send("User is not banned!")
                            return
                        banlist.remove(str(mem.id))
                        await env.set("clink-banlist", "\x00".join(banlist))
                        await ctx.channel.send(f"Lifted ban on {str(mem)}.")

    @commands.command(brief='change another\'s tag')
    async def setusertag(self, ctx):
        msg = ctx.message
        content = msg.content
        author = msg.author
        # is_sfc = await role_checks.stafforcomm(self, msg)
        is_sfc = await stafforcomm(self, msg)
        if is_sfc:
            splits = content.split(' ')
            print(splits)
            if len(splits) < 3 and len(msg.attachments) == 0:
                await ctx.channel.send("Invalid syntax. Usage: `=setusertag @username <tag>`")
            else:
                newtag = ' '.join(splits[2:]) + ' '.join([a.url for a in msg.attachments])
                links = re.findall("(https?://[^\s]+)", newtag)
                if len(newtag) == 0:
                    await ctx.channel.send("Error: your tag is empty, will not store.")
                elif len(newtag) >= MAX_TAG_LEN:
                    await ctx.channel.send("Error: your tag is above {} characters, will not store.".format(MAX_TAG_LEN))
                elif len(links) > 1:
                    await ctx.channel.send("Error: your tag has more than one link and/or attachment, will not store.")
                elif not splits[1].startswith('<@') and not splits[1].endswith('>'):
                    await ctx.channel.send("Invalid syntax (bad mention). Usage: `=setusertag @username <tag>`")
                else:
                    memid = int(splits[1][2:-1].replace('!', ''))
                    to_mem = msg.guild.get_member(memid)
                    print(to_mem)
                    if to_mem is None:
                        await ctx.channel.send("Not a valid mention. Usage: `=setusertag @username <tag>`")
                    else:
                        await env.set("{}_tag_{}".format(ctx.message.guild.id, memid), newtag)
                        await ctx.channel.send("Set {}'s tag.".format(to_mem.display_name))
        else:
            await ctx.channel.send("You are not permitted to use this command.")

    @commands.command(brief="removes specified amount of messages from channel")
    async def purge(self,ctx,amt : int):
        if await stafforcomm(self, ctx.message) == False:
            await ctx.channel.send("You are not permitted to use this command.")
            return
        try:
            deleted = await ctx.channel.purge(limit=amt)
            await ctx.channel.send('Deleted {} message(s)'.format(len(deleted)))
        except discord.errors.Forbidden:
            await ctx.channel.send("Message purge failed; insufficient permissions")

    @commands.command(brief="sets the channel to log breadpins")
    async def pinchannel(self,ctx, chan : discord.TextChannel):
        await env.set(f"{ctx.message.guild.id}-react_channel",chan.id)
        await ctx.channel.send("Breadpin channel set as {}".format(chan.name))

def setup(client):
    client.add_cog(Staff(client))
