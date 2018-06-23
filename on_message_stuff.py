import discord
from discord.ext import commands
import env
user = discord.Member
safe = discord.Object


class on_msg():
    def __init__(self, client):
        self.client = client

    async def on_message(self, message):
        if message.author == self.client.user:
            return  # we do not want the bot to reply to itself
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
