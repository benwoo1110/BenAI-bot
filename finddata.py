import json
from difflib import SequenceMatcher
import traceback


# Load python docs data
with open('code_data.json', 'r') as f:
    all_data = json.load(f)


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def findMatch(value:str, matches:list, acc:float = 0.7):
    highest, matched = 0, None

    for string in matches:
        match = similar(value.lower(), string.lower())
        if (match >= acc or value.lower() in string.lower()) and match > highest:
                highest = match
                matched = string

    return matched


def findAllMatch(value:str, matches:list, acc:float = 0.7):
    matched = []

    for string in matches:
        if value.lower() in string.lower() or similar(value.lower(), string.lower()) >= acc:
            matched.append(string)

    return matched


def Find(code:str, name:str, info:str=None):
    print(name, info)
    try:
        matchedName = findMatch(name, all_data[code].keys())
        if matchedName == None: return None

        get_data = all_data[code][matchedName].copy()

        if info != None:
            info_stuff =  get_data['info']
            get_data['info'] = dict()
            matchedSections = findAllMatch(info, info_stuff.keys())

            if matchedSections == []:
                 get_data['info']['Awwww, Error 404.'] = 'See `!list {}` for sections available.'.format(matchedName)

            else:
                for section in matchedSections:
                    get_data['info'][section] = info_stuff[section]
        
        return get_data

    except:
        traceback.print_stack()
        return

def getNames(code:str = None, name:str = None):
    if code == None: return ', '.join(list(all_data.keys())) + '\n\nRun `!<code> <topic>` to see! For list of topics, run `!list <code>`.'
    
    else: 
        if not code in all_data: return "Actually... idk whats {}... See `!list` for things I know!".format(code)
        elif name == None: return ', '.join(list(all_data[code].keys())) + '\n\nRun `!{0} <name>` to see! For what the section contains, run `!list {0}`.'.format(code)

        else:
            matchedName = findMatch(name, all_data[code].keys())
            if matchedName == None: return "Actually... idk whats {}... See `!list {}` for things I know!".format(name, code)
            return ', '.join(list(all_data[code][matchedName]['info'].keys())) + '\n\nRun `!{} {} [section]` to see!'.format(code, name)

def listCode():
    return list(all_data.keys())