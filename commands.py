import discord
from finddata import Find, getNames, listCode

def Hello(message, contents) -> dict:
    return {
        'type': 'text',
        'data': 'Hello there {}! You can get to know me at `!info`.'.format(message.author.name)
    }


def Code(message, contents) -> dict:
    if len(contents) >= 3: data = Find(contents[0], contents[1], ' '.join(contents[2:]))
    elif len(contents) == 2: data = Find(contents[0], contents[1])
    else: data = None

    if data == None: 
        desc = 'No such {0} documentation found ;(\nSee `!list {0}`.'.format(contents[0])
        embedVar = discord.Embed(title="Hmmmm", description=desc, color=0xff8c00)

    else:
        embedVar = discord.Embed(title=data['title'], url=data['url'], color=0x00ff00)
        
        for name,info in data['info'].items():
            if info == '': continue
            if len(info) > 1024: info = info[:1021]+'...'
            embedVar.add_field(name=name, value=info, inline=False)

    return {
        'type': 'embed',
        'data': embedVar
    }


def List(message, contents) -> dict:
    if len(contents) == 2: 
        title = 'Stuff I know about `{}`:'.format(contents[1])
        list_of_knowledge = getNames(contents[1])

    elif len(contents) >= 3: 
        title = 'Stuff I know about `{} {}`:'.format(contents[1], contents[2])
        list_of_knowledge = getNames(contents[1], contents[2])

    else: 
        title = 'Stuff I know:'
        list_of_knowledge = getNames()
    
    embedVar = discord.Embed(title=title, url='', description=list_of_knowledge, color=0x00ff00)

    return {
        'type': 'embed',
        'data': embedVar
    }



def Info(message, contents) -> dict:
    embedVar = discord.Embed(title='CSF Botty :wave:', description='A fun discord bot that happens to be help(ish) in coding stuff. Run `!commands` to see what I can do!!', color=0xffffff)
    embedVar.add_field(name='Done by:', value='Benedict Woo', inline=False)
    embedVar.add_field(name='Source code:', value='https://github.com/benwoo1110/csf-botty', inline=False)

    return {
        'type': 'embed',
        'data': embedVar
    }


actions = [
    {
        'activate': ['hello', 'sup', 'hi', 'yo'],
        'command': '!hello',
        'info': 'happy to help ;)',
        'runclass': Hello,
    }, 
    {
        'activate': listCode(),
        'command': '!<code> <topic> [section]',
        'info': 'Find info about python! See `!pylist` for all the things I know!',
        'runclass': Code,
    }, 
    {
        'activate': ['list', 'ls'],
        'command': '!list [code] [topic]',
        'info': 'A list of python knowledge I know. If you want to know the topics available, just add the optional parameter `[code]`.',
        'runclass': List,
    }, 
    {
        'activate': ['info', 'about', 'whoareyou'],
        'command': '!info',
        'info': 'About me xD',
        'runclass': Info,
    }, 
]

def runCommand(message, contents):
    for action in actions:

        # Check for commands
        if contents[0] in action['activate']:
            return action['runclass'](message, contents)

        # special for help command
        elif contents[0] in  ['commands', 'command', 'cmd']:
            embedVar = discord.Embed(title='Commands', color=0x0000ff)
            for a in actions:
                embedVar.add_field(name=a['command'], value=a['info'], inline=False)

            return {
                'type': 'embed',
                'data': embedVar
            }

    # Command is not found
    embedVar = discord.Embed(title="Sorry idk mate ;(", description='Unknown command, see `!cmd` for commands available.', color=0xff8c00)

    return {
        'type': 'embed',
        'data': embedVar
    }