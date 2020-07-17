import json
from difflib import SequenceMatcher
import traceback


# Load python docs data
with open('python_data.json', 'r') as f:
    python_data = json.load(f)


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


def Find(name:str, info:str=None):
    print(name, info)
    try:
        matchedName = findMatch(name, python_data.keys())
        if matchedName == None: return None

        get_data = python_data[matchedName].copy()

        if info != None:
            info_stuff =  get_data['info']
            get_data['info'] = dict()
            matchedSections = findAllMatch(info, info_stuff.keys())

            if matchedSections == []:
                 get_data['info']['Awwww, Error 404.'] = 'See `!pylist {}` for sections available.'.format(matchedName)

            else:
                for section in matchedSections:
                    get_data['info'][section] = info_stuff[section]
        
        return get_data

    except:
        traceback.print_stack()
        return

def getNames(name:str = None):
    if name == None: return ', '.join(list(python_data.keys())) + '\n\nRun `!py <name>` to see!'

    else:
        matchedName = findMatch(name, python_data.keys())
        if matchedName == None: return "Actually... i dont know... See `!pylist` for things I know!"
        
        return ', '.join(list(python_data[matchedName]['info'].keys())) + '\n\nRun `!py {} [section]` to see!'.format(name)
