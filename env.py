import os
import asyncio


async def set(name, value, tries=5, timeout=2):
    os.environ[name] = str(value)


async def get(name, tries=5, timeout=2):
    return os.environ[name]
