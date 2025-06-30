glob_singleton = {}

from .Keyboard import Keyboard

keys = Keyboard.get_key_list()

def keep_open(*args, **kwargs):
    pass


class Game_Context:
    def __init__(self, events, keys):
        self.events = events
        self.keyboard = keys

        self.event_args = {
            "on_key_down"  : None,
            "on_key_up"    : None,
            "on_mouse_down": None,
            "on_mouse_up"  : None,
            "on_mouse_move": None,
            "on_close": None
        }
