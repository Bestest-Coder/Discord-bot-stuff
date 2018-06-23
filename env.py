import os


def set(name, value):
    os.environ[name] = value


def get(name):
    return os.environ[name]
