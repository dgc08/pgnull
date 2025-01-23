glob_singleton = {}

from .Keyboard import Keyboard

keys = Keyboard.get_key_list()

def keep_open(*args, **kwargs):
    pass


class Game_Context:
    def __init__(self, events, keys):
        self.events = events
        self.keyboard = keys
