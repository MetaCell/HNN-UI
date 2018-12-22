import os
import json
import operator
from functools import reduce

def push_keys(dicctionary={}, keys=[]):
    '''
    It creates all keys listed in "keys" 
    nesting them inside "dicctionary".
    It does not affects what already exists
    '''
    if not keys[0] in dicctionary.keys(): 
        dicctionary[keys[0]] = {}
    for i in range(len(keys)):
        try:
            reduce(operator.getitem, keys[:i+1], dicctionary)
        except:
            reduce(operator.getitem, keys[:i], dicctionary)[keys[i]] = {}


def load_metadata(directory):
    '''
    Explores dir folder and subfolders looking for JSON files.
    Each JSON file is dumped in a dicctionary where the keys
    represent the directory path
    '''
    meta = {}
    for root, _, files in os.walk(directory):
        for name in files:
            if name.endswith((".json")):
                keys = root.split('/')
                push_keys(meta, keys)
                with open(f"{root}/{files[0]}") as file:
                    reduce(operator.getitem, keys[:-1], meta)[keys[-1]] = json.load(file)
    
    # remove leading keys that belong to "directory path"
    return reduce(operator.getitem, directory.split('/'), meta)