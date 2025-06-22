# Dieses Dictionary hält globale variablen, damit pgnull objekte etwa auf das Game Object zugreifen können
# in zukunft sollten alle anwendungsfälle dies ganz durch eine self.parent logic wie bei GameObject ersetzt werden,
# sodass dies dann deprecated werden kann
glob_singleton = {}

from .Keyboard import Keyboard

# eine liste an allen Key Codes
keys = Keyboard.get_key_list()

# im prinzip `pass` als function
def keep_open(*args, **kwargs):
    pass

class Game_Context:
    def __init__(self, events, keys):
        self.events = events
        self.keyboard = keys
