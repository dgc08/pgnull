glob_singleton = {}

from .Keyboard import Keyboard

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


class Game_Events:
    @staticmethod
    def on_update(context):
        pass

    @staticmethod
    def on_start(context):
        pass

    @staticmethod
    def on_iteration_start():
        pass

    @staticmethod
    def on_close():
        pass

    @staticmethod
    def on_draw():
        pass

    @staticmethod
    def on_predraw():
        pass

    @staticmethod
    def on_mouse_down(pos, button):
        pass

    @staticmethod
    def on_mouse_up(pos, button):
        pass

    @staticmethod
    def on_mouse_move(pos, rel, buttons):
        pass

    @staticmethod
    def on_key_down(key):
        pass

    @staticmethod
    def on_key_up(key):
        pass
