from .utils import glob_singleton

from pygame.math import Vector2

class Scene():
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
        self.pos = Vector2(0,0)

        self.static = False
        self.active = True
        self.__dequeued = False
        self.parent = None

    def add_game_object(self, game_obj):
        game_obj.parent = self
        self._game_objs.append(game_obj)
        game_obj.start()

   # def remove_game_object(self, game_obj):
   #     # use dequeue instead
   #     self._game_objs.remove(game_obj)

    def register_object(self, game_obj, name):
        setattr(self, name, game_obj)
        self.add_game_object(game_obj)

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
                if g.static:
                    g.draw()
                else:
                    g.pos += self.pos
                    g.draw()
                    g.pos -= self.pos
        self.on_draw()


    def do_update(self, ctx):
        self.on_update(ctx)
        for g in self._game_objs:
            if g.is_dequeued():
                self._game_objs.remove(g)
                del g
                continue
            if g.active:
                g.update(ctx)

    # copy paste from GameObject because we can't inherit from there due to circular import issues

    def is_dequeued(self):
        return self.__dequeued

    def dequeue(self):
        self.__dequeued = True

        # Delete yourself from the current scene
        # We do not do that anymore because this approach is not fit
        #Game.get_game().scene.remove_game_object(self)

    def draw(self, ):
        self.do_draw()
    def update(self, ctx):
        self.do_update(ctx)
    def start(self):
        self.on_start()
