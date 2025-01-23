from .utils import glob_singleton

class Scene:
    @staticmethod
    def on_update(context):
        pass

    @staticmethod
    def on_start():
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


    def __init__(self, background_color=None):
        self.color = background_color
        self._game_objs = []

    def add_game_object(self, game_obj):
        self._game_objs.append(game_obj)
    def remove_game_object(self, game_obj):
        self._game_objs.remove(game_obj)

    def register_event(self, event: str, event_runnable):
        if not callable(event_runnable):
            raise TypeError("event_runnable isn't callable (It needs to be a reference to a function that can be executed)")

        self.__setattr__(event, event_runnable)
        return

    def event(self, event_name: str):
        def decorator(func):
            self.register_event(event_name, func)
            return func
        return decorator

    def do_draw(self):
        if self.color:
            glob_singleton["game"].screen.fill(self.color)
        self.on_predraw()
        for g in self._game_objs:
            if g.active:
                g.draw()
        self.on_draw()


    def do_update(self, ctx):
        self.on_update(ctx)
        for g in self._game_objs:
            if g.active:
                g.update(ctx)
