# Import modules
import discord
from finddata import Find
import traceback
import os


# Check if token file exist
if not os.path.isfile('TOKEN.txt'):
    with open('TOKEN.txt', 'w') as tokenFile:
        tokenFile.write('INSERT_TOKEN_HERE')
        tokenFile.close()
    print('Please key in the bot token in TOKEN.txt and run the program again.')
    exit()

# Get the bot token
with open('TOKEN.txt', 'r') as tokenFile:
    TOKEN = tokenFile.read().rstrip()
    tokenFile.close()


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
        
        if contents[0] == ('!hello'):
            await message.channel.send('Hello there {}!'.format(message.author.name))

        elif contents[0] == ('!test'):
            embedVar = discord.Embed(title="Title", url='https://www.google.com', color=0x00ff00)
            embedVar.add_field(name="Field1", value="hi", inline=False)
            embedVar.add_field(name="Field2", value="hi2", inline=False)
            await message.channel.send(embed=embedVar)

        elif contents[0] == ('!py'):
            try:
                if len(contents) >= 3: data = Find(contents[1], ''.join(contents[2:]))
                else: data = Find(contents[1])

                if data == None: 
                    traceback.print_exc()
                    embedVar = discord.Embed(title="Hmmmm", description='No such python documentation found ;(\nSee `!pyhelp`.', color=0xff8c00)
                    await message.channel.send(embed=embedVar)

                else:
                    embedVar = discord.Embed(title=data['title'], url=data['url'], color=0x00ff00)
                    
                    for name,info in data['info'].items():
                        if info == '': continue
                        if len(info) > 1024: info = info[:1021]+'...'
                        embedVar.add_field(name=name, value=info, inline=False)

                    embedVar.set_footer(text='requested by {} | resource from w3schools.com'.format(message.author.name))

                    await message.channel.send(embed=embedVar)

            except:
                traceback.print_exc()
                embedVar = discord.Embed(title="Oh NooOoO", description='An error occurred. Please try again...', color=0xff0000)
                await message.channel.send(embed=embedVar)
            

# Init the bot
client = discord.Client()

# Enable the bot
client = MyClient()
client.run(TOKEN)