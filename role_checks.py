import env
import discord
import asyncio

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


def ifcomm(self, inp):
    if inp.author.id in self.client.commanderids:
        return True
    else:
        return False


def ifvip(self, inp):
    if inp.author.id in self.client.commanderids:
        return True
    if inp.guild.owner == inp.author:
        return True
    if inp.author.guild_permissions.administrator is True:
        return True
    else:
        return False
