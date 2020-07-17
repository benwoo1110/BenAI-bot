# Import modules
import discord
import traceback
import os
import re
from finddata import *


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
        # ignore if by the bot itself
        if message.author == client.user: return

        # Split contents into each words
        contents = message.content.rstrip().split()
        if len(contents) < 1: return

        # Commands to run
        if contents[0].startswith('!'):
            try:
                # Remove all non alphabets
                contents[0] = re.sub(r'\W+', '',  contents[0])

                if contents[0] in ['hello', 'sup', 'hi', 'yo']:
                    await message.channel.send('Hello there {}! You can get to know me at `!info`.'.format(message.author.name))
                    return

                elif contents[0] in ['py', 'python']:
                    
                        if len(contents) >= 3: data = Find(contents[1], ' '.join(contents[2:]))
                        elif len(contents) == 2: data = Find(contents[1])
                        else: data = None

                        if data == None: 
                            embedVar = discord.Embed(title="Hmmmm", description='No such python documentation found ;(\nSee `!pylist`.', color=0xff8c00)

                        else:
                            embedVar = discord.Embed(title=data['title'], url=data['url'], color=0x00ff00)
                            
                            for name,info in data['info'].items():
                                if info == '': continue
                                if len(info) > 1024: info = info[:1021]+'...'
                                embedVar.add_field(name=name, value=info, inline=False)
                
                elif contents[0] in ['pylist', 'pythonlist']:
                    if len(contents) >= 2: 
                        title = 'I know these about `{}`:'.format(contents[1])
                        list_of_knowledge = getNames(contents[1])
                    else: 
                        title = 'I know these:'
                        list_of_knowledge = getNames()
                    
                    embedVar = discord.Embed(title=title, url='https://www.w3schools.com/python/', description=list_of_knowledge, color=0x00ff00)

                elif contents[0] in ['pyhelp', 'pythonhelp']:
                    embedVar = discord.Embed(title='Commands', color=0x0000ff)
                    embedVar.add_field(name='!hello', value='happy to help ;)', inline=False)
                    embedVar.add_field(name='!py <name> [section]', value='Find info about python! See `!pylist` for all the things I know!', inline=False)
                    embedVar.add_field(name='!pylist [name]', value='A list of python knowledge I know. If you want to know the sections for that name, just add the optional parameter `[name]`.', inline=False)
                    embedVar.add_field(name='!info', value='About me xD', inline=False)

                elif contents[0] in ['info']:
                    embedVar = discord.Embed(title='CSF Botty :wave:', description='A fun discord bot that happens to be help(ish) in python. Run `!pyhelp` to see what I can do!!', color=0xffffff)
                    embedVar.add_field(name='Done by:', value='Benedict Woo', inline=False)
                    embedVar.add_field(name='Source code:', value='https://github.com/benwoo1110/csf-botty', inline=False)

                else:
                    embedVar = discord.Embed(title="Sorry idk mate ;(", description='Unknown command, see `!pyhelp` for commands available.', color=0xff8c00)

            except Exception as e:
                traceback.print_exc()
                embedVar = discord.Embed(title="Oh NooOoO!", description='Beep Beep Boop Boop I errored out.```'+str(e)+'```', color=0xff0000)
            
            # Set footnote
            embedVar.set_footer(text='requested by {} | resource from w3schools.com'.format(message.author.name))

            await message.channel.send(embed=embedVar)
            return
            

# Init the bot
client = discord.Client()

# Enable the bot
client = MyClient()
client.run(TOKEN)