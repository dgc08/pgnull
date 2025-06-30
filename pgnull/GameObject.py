from .utils import glob_singleton

from pygame.math import Vector2

# This works the same as a Node in Godot
class GameObject():
    def on_update(self, context):
        pass

    def on_start(self, ):
        pass

    def on_close(self, ):
        pass

    def on_draw(self, ctx):
        pass

    def on_mouse_down(self, pos, button):
        pass

    def on_mouse_up(self, pos, button):
        pass

    def on_mouse_move(self, pos, rel, buttons):
        pass

    def on_key_down(self, key):
        pass

    def on_key_up(self, key):
        pass

    def __init__(self):
        self.bg_color = None
        self.__game_objs = []
        self._name_map = {}

        self.pos = Vector2(0,0)
        if not hasattr(self, "height"):
            self.height = 0
            self.width = 0

        self.static = False
        self.active = True
        self.parent = None

    def add_game_object(self, game_obj):
        game_obj.parent = self
        self.__game_objs.append(game_obj)
        game_obj.on_start()

   # def remove_game_object(self, game_obj):
   #     # use dequeue instead
   #     self.__game_objs.remove(game_obj)

    #short name on purpose
    def reg_obj(self, game_obj, name=None):
        if name:
            setattr(self, name, game_obj)
            self._name_map[id(game_obj)] = name

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

    def do_update(self, ctx):
        #in analogy to draw, update yourself first
        self.on_update(ctx)

        # check all your event listeners
        for listener in ctx.event_args:
            if ctx.event_args[listener] is None:
                pass
            else:
                getattr(self, listener)(*ctx.event_args[listener]) # call your listener

        for g in self.__game_objs[:]: # safe iteration while modifying list
            if g.active:
                g.do_update(ctx)

    def do_draw(self, ctx):
        # draw is same as update, just later and the GameObjects offset the pos of their children according to their own pos
        if self.bg_color:
            # in case there is a background color set
            # please do only use this for one scene in the tree
            glob_singleton["game"].screen.fill(self.bg_color)
        # draw children last -> draw children on top of you
        self.on_draw(ctx)
        for g in self.__game_objs[:]:
            if g.active:
                if g.static:
                    g.do_draw(ctx)
                else:
                    g.pos += self.pos
                    g.do_draw(ctx)
                    g.pos -= self.pos

    def perform_dequeue_for(self, g):
        # perfom dequeue for given child
        # this is usually only called by the child's .dequeue()
        self.__game_objs.remove(g)
        name = self._name_map.pop(id(g), None)
        if name and hasattr(self, name):
            delattr(self, name)

    def get_children(self):
        return self.__game_objs.copy()

    def dequeue(self):
        self.parent.perform_dequeue_for(self)
