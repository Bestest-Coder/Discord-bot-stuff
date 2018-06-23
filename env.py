import os


def set(name, value):
    os.environ[name] = str(value)


def get(name):
    return os.environ[name]
