import discord
from discord.ext import commands
import asyncio
import env
user = discord.Member


def stafforcomm(self, inp):
    if self.client.commanderid == inp.author.id:
        return True
    server_stfrole = int(env.get('{}_stfrole'.format(str(inp.guild.id))))
    # if server_stfrole == discord.utils.get(inp.author.roles, id=server_stfrole).id:  # check to make sure the ids are the same
    if server_stfrole in [role.id for role in inp.author.roles]:
        return True
    else:
        return False


def ifcomm(self, inp):
    if self.client.commanderid == inp.author.id:
        return True
    else:
        return False


def ifvip(self, inp):
    if self.client.commanderid == inp.author.id:
        return True
    if inp.guild.owner == inp.author:
        return True
    if inp.author.guild_permissions.administrator is True:
        return True
    else:
        return False


class Staff():
    def __init__(self, client):
        self.client = client

    @commands.command(brief='sends a message to warning channel')
    async def warn(self, ctx, war_user: user, *, reason: str):
        if stafforcomm(self, ctx.message) is False:
            print(str(ctx.author) + " tried to warn but isn't staff")
            return
        #com_send = ctx.author
        if reason is None:
            reason = ''
        msg = (war_user.mention + ', you have recieved a warning for '
               ) + reason  #  + ', this is warning #' + str(war_user.warns) + 'at the hands of ' + str(com_send)
        wchan_id = int(env.get('{}_wchan'.format(str(ctx.message.guild.id))))
        wchan = discord.utils.get(client.get_all_channels(), id=wchan_id)  # get real channel behind the id
        await wchan.send(msg)
        #print((((str(ctx.author) + ': ') + str(war_user)) + ' has been warned for: ') + reason)

    @commands.command(brief="set's the warning channel")
    async def wchan(self, ctx, wchan: discord.TextChannel):
        if ifcomm(self, ctx.message) is False:
            return
        # self.client.data[str(ctx.message.guild.id)]['wchan'] = wchan.id
        to_set = '{}_wchan'.format(str(ctx.message.guild.id))
        env.set(to_set, wchan.id)  # set the wchan id with var name guildid_wchan
        msg = 'Warning channel is ' + str(wchan)
        await ctx.channel.send(msg)
        #print((str(ctx.author) + ': ') + msg)

    @commands.command(brief='makes the bot say the content')
    async def say(self, ctx, *, content: str):
        if stafforcomm(self, ctx.message) is False:
            return
        await ctx.channel.send(content.format(ctx.message))
        await ctx.message.delete()
        #print(((str(ctx.author) + ': ') + 'Bot said : ') + content)

    @commands.command(brief='say but less suspiscous')
    async def dsay(self, ctx, *, content: str):
        if stafforcomm(self, ctx.message) is False:
            return
        dest = ctx.channel
        dur = len(ctx.message.content) * 0.1
        await ctx.message.delete()
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
        env.set('{}_stfrole'.format(str(ctx.message.guild.id)), staffrole.id)  # set guildid_stfrole to the given staffrole's id
        msg = 'staff role has been set to ' + str(staffrole)
        await ctx.channel.send(msg)
        #print((str(ctx.author) + ': ') + msg)

    @commands.command(brief="Sets the bot's nickname")
    async def nick(self, ctx, *, name: str):
        if stafforcomm(self, ctx.message) is False:
            return
        await ctx.message.guild.me.edit(nick=name)
        await ctx.channel.send('Nickname is now "' + name + '"')


def setup(client):
    client.add_cog(Staff(client))
