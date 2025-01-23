from .Game import Game

class GameObject:
    def __init__(self):
        self.active = True

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

    def draw(self, ):
        pass
    def update(self, ctx):
        pass
