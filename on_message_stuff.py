import discord
from discord.ext import commands
import env


CLINK_NAME = "clink"
user = discord.Member
safe = discord.Object


async def get_clink_toggle(sid):
    try:
        ct = await env.get(str(sid) + "-clink_toggle")
        ct = bool(int(ct))
    except env.GetReturnedNothing:
        ct = True
    return ct


class on_msg():
    def __init__(self, client):
        self.client = client

    async def on_message(self, message):
        if message.author == self.client.user:
            return  # we do not want the bot to reply to itself

        if message.channel.name == CLINK_NAME:  # for now, let's have all bots be able to send their messages through
            this_clink_toggle = await get_clink_toggle(message.guild.id)
            if this_clink_toggle:  # if they want to send messages
                for guild in self.client.guilds:  # for each server
                    x = await get_clink_toggle(guild.id)
                    if x:  # if this server wants to get messages
                        for channel in guild.channels:  # send
                            if channel.id != message.channel.id:
                                if channel.name == CLINK_NAME:  # the
                                    msg = message.content
                                    msg = msg.replace("@", "(at)")  # gets rid of @here and @everyone
                                    for mention in msg.mentions:
                                        msg = msg.replace(mention.mention, f"(at){mention.name}".replace("@", "(at)"))  # removes all mentions
                                    channel.send(f"({message.guild.name}) - {msg}")  # message

        if message.author.bot is True:
            return
        for i in range(len(message.mentions)):
            if message.mentions[i] == self.client.user:
                await message.channel.send('the fuck you want {0.author.mention}'.format(message))
        if message.content[0:2] == 'r/':
            msg = 'Did you mean: https://reddit.com/' + message.content
            await message.channel.send(msg)
    '''
        for i in range(len(message.content)):
            if message.content[i:i+4] == 'fuck' or message.content[i:i+4] == 'shit' or message.content[i:i+5] == 'bitch':
                #msg = '[insert christian server joke here]'.format(message)
                #await self.client.send_message(message.channel, msg)
                await self.client.delete_message(message)
    '''

    '''
        #if message.content.startswith('Ruddy'):
            #msg = 'all hail our lord and savior'.format(message)
            #await self.client.send_message(message.channel, msg)
            #time.sleep(600)

        #if message.content.startswith('gaster'):
            #msg = 'Ban gaster'.format(message)
            #await self.client.send_message(message.channel, msg)

        #if message.content.startswith('billy mays'):
            #msg = 'Drink Oxiclean!'.format(message)
            #await self.client.send_message(message.channel, msg)

        #if message.content.startswith('hayden'):
            #msg = "We do not speak it's name!".format(message)
            #await self.client.send_message(message.channel, msg)

        #if message.content.startswith('gandy'):
            #msg = 'Theif of the least dank memes'.format(message)
            #await self.client.send_message(message.channel, msg)
    '''


def setup(client):
    client.add_cog(on_msg(client))
