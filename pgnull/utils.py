glob_singleton = {}

from pgnull.Keyboard import Keyboard

keys = Keyboard.get_key_list()


class Colors:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    PINK = (255, 192, 203)

def keep_open(*args, **kwargs):
    pass

class Game_Context:
    def __init__(self, events, keys):
        self.events = events
        self.keyboard = keys

