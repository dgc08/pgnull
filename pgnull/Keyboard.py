import pygame.locals

class Keyboard:
    def __init__(self):
        self.keys = {}
        # alle pygame.locals durchgehen, wo auch alle tasten der tastatur hinterlegt sind
        # man nimmt die keys, entfernt das K_ und set es sich selbst al attribut
        # dadurch wird dann so etwas wie keyboard_obj.a == True wenn taste a gedrückt wird möglich
        # In Game.py werden die keys auf True bzw False gesetzt

        # Es wird gleichzeitig auch self.keys immer geupdated, damit man dort zb über alle keys iterieren kann
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