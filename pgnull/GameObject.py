from .Game import Game

from pygame.math import Vector2

class GameObject:
    def __init__(self):
        self.active = True
        self.static = False

        self.__dequeued = False

        self.parent = None

    def register_event(self, event: str, event_runnable):
        if not callable(event_runnable):
            raise TypeError("event_runnable isn't callable (It needs to be a reference to a function that can be executed)")

        self.__setattr__(event, event_runnable)
        return

    # dummy attribute, if you yourself are being drawn in some way you should replace this
    @property
    def pos(self) -> Vector2:
        return Vector2(0,0)
    @pos.setter
    def pos(self, value):
        pass

    def event(self, event_name: str):
        def decorator(func):
            self.register_event(event_name, func)
            return func
        return decorator

    def is_dequeued(self):
        return self.__dequeued

    def dequeue(self):
        self.__dequeued = True

        # Delete yourself from the current scene
        # We do not do that anymore because this approach is not fit
        #Game.get_game().scene.remove_game_object(self)

    def draw(self, ):
        pass
    def update(self, ctx):
        pass
    def start(self):
        pass
