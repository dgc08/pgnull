glob_singleton = {}

from pygame.math import clamp, Vector2
from .Keyboard import Keyboard

keys = Keyboard.get_key_list()

def keep_open(*args, **kwargs):
    pass


class Game_Context:
    def __init__(self, events, keys):
        self.events = events
        self.keyboard = keys
        self.mouse = [False, False, False, False, False]

        self.mouse_rel = (0,0)

        self.event_args = {
            "on_key_down"  : None,
            "on_key_up"    : None,
            "on_mouse_down": None,
            "on_mouse_up"  : None,
            "on_mouse_move": None,
            "on_close": None
        }


def clamp_vector(orig, minv, maxv=Vector2(float("inf"), float("inf"))):
    return (clamp(orig.x, minv.x, maxv.x), clamp(orig.y, minv.y, maxv.y))
