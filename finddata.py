import json
from difflib import SequenceMatcher
import traceback

with open('python_data2.json', 'r') as f:
    python_data = json.load(f)

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def Find(name:str, info:str=None):
    try:
        highest = 0
        get_data = None
        for title,data in python_data.items():
            match = similar(title, name)
            if (match >= 0.7 or name in title) and match > highest:
                highest = match
                get_data = data.copy()

        if info != None:
            info_stuff = {}
            for key,value in get_data['info'].items():
                if info.lower() in key.lower() or similar(info.lower(), key.lower()) >= 0.7:
                    info_stuff[key] = value


            get_data['info'] = info_stuff
        
        return get_data

    except:
        traceback.print_stack()
        return None

def getNames():
    pass