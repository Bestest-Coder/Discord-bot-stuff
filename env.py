import os
import random
import asyncio
import websockets


NOT_HEROKU, HEROKU = [r(10,99) for r in (random.randint,)*2]

try:
    KEY = os.environ['SILI_SECRET']
    PLATFORM = HEROKU
except KeyError:
    PLATFORM = NOT_HEROKU
    KEY = ''
print(PLATFORM)


class GetReturnedNothing(Exception):
    def __init__(self, message):
        self.message = message


async def set_old(name, value):
    os.environ[name] = str(value)


async def get_old(name):
    return os.environ[name]


async def set(name, value, tries=5, timeout=2):
    if PLATFORM == HEROKU:
        while tries:
            try:
                async with websockets.connect('ws://siliconwolf.pw:12345', timeout=timeout) as sock:
                    pack = "set|{}|{}|{}".format(name, value, KEY)
                    await sock.send(pack)
                    await sock.recv()  # dummy recieve so as to not hang the server
                    tries = 0
            except websockets.exceptions.ConnectionClosed:
                tries -= 1
    elif PLATFORM == NOT_HEROKU:
        await set_old(name, value)
    else:
        raise Exception('why the fuck is PLATFORM not NOT_HEROKU nor HEROKU')


async def get(name, tries=5, timeout=2):
    if PLATFORM == HEROKU:
        while tries:
            try:
                async with websockets.connect('ws://siliconwolf.pw:12345', timeout=timeout) as sock:
                    pack = "get|{}|{}".format(name, KEY)
                    await sock.send(pack)
                    # data = await sock.recv()
                    data = await sock.recv()
                    return data
                    tries = 0  # hopefully doesn't execute
            except websockets.exceptions.ConnectionClosed:
                tries -= 1
        raise GetReturnedNothing("returned nothing")
    elif PLATFORM == NOT_HEROKU:
        await get_old(name)
    else:
        raise Exception('why the fuck is PLATFORM not NOT_HEROKU nor HEROKU')


'''
def ez(func):
    asyncio.get_event_loop().run_until_complete(func)


def set(name, value):
    ez(_set(name, value))


def get(name):
    global RESULT
    RESULT = GetReturnedNothing('get call returned nothing')
    ez(_get(name))
    return RESULT
'''
