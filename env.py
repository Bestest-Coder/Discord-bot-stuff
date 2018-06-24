import os
import asyncio
import websockets

try:
    KEY = os.environ['SILI_SECRET']
except KeyError:
    print('cryyyy')
    KEY = 'abcdefg'
RESULT = ''


def set_old(name, value):
    os.environ[name] = str(value)


def get_old(name):
    return os.environ[name]


async def _set(name, value, tries=5):
    while tries:
        try:
            async with websockets.connect('ws://siliconwolf.pw:12345', timeout=2) as sock:
                pack = "set|{}|{}|{}".format(name, value, KEY)
                await sock.send(pack)
                await sock.recv()  # dummy recieve so as to not hang the server
                tries = 0
        except websockets.exceptions.ConnectionClosed:
            tries -= 1


async def _get(name, tries=5):
    global RESULT
    while tries:
        try:
            async with websockets.connect('ws://siliconwolf.pw:12345', timeout=2) as sock:
                pack = "get|{}|{}".format(name, KEY)
                await sock.send(pack)
                data = await sock.recv()
                RESULT = data
                tries = 0
        except websockets.exceptions.ConnectionClosed:
            tries -= 1


def ez(func):
    asyncio.get_event_loop().run_until_complete(func)


def set(name, value):
    ez(_set(name, value))


class GetReturnedNothing(Exception):
    def __init__(self, message):
        self.message = message


def get(name):
    global RESULT
    RESULT = GetReturnedNothing('get call returned nothing')
    ez(_get(name))
    return RESULT
