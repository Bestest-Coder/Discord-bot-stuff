import os
import asyncio
import pickle


db = pickle.load(open("db.pkl", "rb"))

async def set(name, value, tries=5, timeout=2):
    db['bestest'][name] = str(value)
    pickle.dump(db, open("db.pkl", "wb"))

async def get(name, tries=5, timeout=2):
    try:
        return db['bestest'][name]
    except KeyError:
        return 'variable does not exist'
