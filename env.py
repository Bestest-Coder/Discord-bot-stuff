import os
import asyncio
import pickle

#if either of these gets uploaded to github sometihng went VERY WRONG
db = pickle.load(open("db.pkl", "rb"))
tokenfile = open("tokens.txt", "r")

lines = tokenfile.readlines()

async def set(name, value, tries=5, timeout=2):
    db['bestest'][name] = str(value)
    pickle.dump(db, open("db.pkl", "wb"))

async def get(name, tries=5, timeout=2):
    try:
        return db['bestest'][name]
    except KeyError:
        return 'variable does not exist'

def tokenget(line):
    return lines[line][:-1] #0 is bot token, 1 is BFD token
