from .utils import glob_singleton

from pygame.math import Vector2

# Das ganze spiel ist ein Tree aus GameObjects, alles ist ein GameObject
# Hierbei habe ich mich von Godots Node-System inspirieren lassen
# Game() hält einen Root-Node, dem alle anderen GameObjects untergeordnet sind
# Jedes GameObject sorgt dafür, dass draw und update von ihren Kindern ausgeführt wird
class GameObject():
    def on_update(self, context):
        pass

    def on_start(self, ):
        pass

    def on_iteration_start(self, ):
        # this is not propagated, on the main scene it acts like a pre-update
        # this is called by the game at the very start of the game loop
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
        self.__game_objs = [] # die kinder von self
        self._name_map = {}

        self.pos = Vector2(0,0)
        if not hasattr(self, "height"):
            self.height = 0
            self.width = 0

        self.static = False
        self.active = True
        self.parent = None

    def add_game_object(self, game_obj):
        game_obj.parent = self # kind.parent ist eine referenz zu self
        self.__game_objs.append(game_obj)
        game_obj.on_start()

   # use dequeue instead
   # def remove_game_object(self, game_obj):
   #     self.__game_objs.remove(game_obj)

    #short name on purpose
    def reg_obj(self, game_obj, name=None):
        if name:
            setattr(self, name, game_obj)
            self._name_map[game_obj] = name # das sorgt dafür, dass wenn ein gameobj unter einem namen gespeichtert wird die referenz unter dem namen beim dequeuen auch gelöscht wird
            # ansonsten würde der Garbage Collector nicht das Objekt löschen, da noch eine referenz vorhanden ist
            # dieser approach ist suboptimal und sollte in zukunft verbessert werden
            # außerdem enstehen probleme mit un-hashbaren objekten, da diese nicht als key für ein Dict verwendet werden können
            # TODO

        self.add_game_object(game_obj)

    def register_event(self, event: str, event_runnable):
        if not callable(event_runnable):
            raise TypeError("event_runnable isn't callable (It needs to be a reference to a function that can be executed)")

        self.__setattr__(event, event_runnable)
        return

    # dies ermöglicht es, eine funktion als methode eines bereits vorhandenen objektes zu registrieren
    # sodass man nicht unbedingt eine neue erbende klasse schreiben muss
    def event(self, event_name: str):
        def decorator(func):
            self.register_event(event_name, func)
            return func
        return decorator

    def do_update(self, ctx):
        # do_update bzw do_draw des root nodes werden vom Game() aufgerufen
        # diese rufen dann rekursiv dieselbe funktion auf all ihre kinder auf, wodurch der ganze tree abgearbeitet wird

        #in analogy to draw, update yourself first
        self.on_update(ctx)
        for g in self.__game_objs[:]: # safe iteration while modifying list
            if g.active:
                g.do_update(ctx)

    def do_draw(self, ctx):
        # draw ist dasselbe wie update, nur später in der game loop und die GameObjects verschieben die position ihrer kinder entsprechend ihrer eigenen position
        if self.bg_color:
            # in case there is a background color set
            # please do only use this for one object in the tree
            glob_singleton["game"].screen.fill(self.bg_color)
        # draw yourself first, then draw children -> Kinder werden über self gezeichnet
        self.on_draw(ctx)
        for g in self.__game_objs[:]:
            if g.active:
                if g.static: # static bedeutet, das objekt wird nich durch offseten beeinflusst
                              # dies ist hilfreich, wenn man ein HUD programmiert, das nicht durch offseten des Root Nodes,
                              # wenn die "Kamera" sich bewegt, beeinflusst wird und an ort und stelle bleibt
                    g.do_draw(ctx)
                else:
                    # bevor draw weiter rekursiv ausgeführt wird, offseten
                    g.pos += self.pos
                    g.do_draw(ctx)
                    g.pos -= self.pos

    def perform_dequeue_for(self, g):
        # perfom dequeue for given child
        # this is usually only called by the child's .dequeue()
        self.__game_objs.remove(g)
        name = self._name_map.pop(g, None)
        if name and hasattr(self, name):
            delattr(self, name)

    def get_children(self):
        return self.__game_objs.copy() # copy, sodass durch das modifizieren der zurückgebenen Liste nicht die originale modifiziert wird

    def dequeue(self):
        self.parent.perform_dequeue_for(self) # Das Parent soll einen löschen
