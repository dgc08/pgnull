import pygame.locals

class Keyboard:
    def __init__(self):
        self.keys = {}
        for i in dir(pygame.locals):
            if i.startswith("K_"):
                key = getattr(pygame.locals, i)
                setattr(self, i.replace("K_", "").lower(), False)
                self.keys[i.replace("K_", "").lower()] = False

    def set_key(self, key, value):
        setattr(self, key, value)
        self.keys[key] = value

    @classmethod
    def get_key_list(cls):
        return Keyboard().keys.keys()