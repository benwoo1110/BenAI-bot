# Import modules
import discord
import traceback
import os
import re
from finddata import getNames, Find
from commands import runCommand


# Check if token file exist
if not os.path.isfile('TOKEN.txt'):
    with open('TOKEN.txt', 'w') as tokenFile:
        tokenFile.write('INSERT_TOKEN_HERE')
        tokenFile.close()
    print('Please key in the bot token in TOKEN.txt and run the program again. On how to get a bot: https://discordpy.readthedocs.io/en/latest/discord.html')
    exit()

# Get the bot token
with open('TOKEN.txt', 'r') as tokenFile:
    TOKEN = tokenFile.read().rstrip().lstrip()
    tokenFile.close()

# Token isnt there
if TOKEN == 'INSERT_TOKEN_HERE':
    print('Please key in the your bot token in TOKEN.txt and run the program again. On how to get a bot: https://discordpy.readthedocs.io/en/latest/discord.html')
    exit()
    

# Bot class
class MyClient(discord.Client):

    # Bot init message
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    # When a message is sent
    async def on_message(self, message):
        try:
            # ignore if by the bot itself
            if message.author == client.user: return

            # Split contents into each words
            contents = message.content.rstrip().split()
            if len(contents) < 1: return

            # Commands to run
            if contents[0].startswith('!'):
                    # Remove all non alphabets
                    contents[0] = contents[0].split('!')[-1].lower()

                    cmd_output = runCommand(message, contents)
                    
                    if cmd_output['type'] == 'embed':
                        # Set footnote
                        cmd_output['data'].set_footer(text='requested by {} | resource from w3schools.com'.format(message.author.name))
                        await message.channel.send(embed=cmd_output['data'])

                    elif cmd_output['type'] == 'text':
                        await message.channel.send(cmd_output['data'])

        except Exception as e:
            traceback.print_exc()
            embedVar = discord.Embed(title="Oh NooOoO!", description='Beep Beep Boop Boop I errored out.```'+str(e)+'```', color=0xff0000)
            await message.channel.send(embed=embedVar)


# Init the bot
client = discord.Client()
client = MyClient()


# Enable the bot
def run():
    client.run(TOKEN)