from .GameObject import GameObject

class VPane(GameObject):
    def __init__(self, element_gap):
        super().__init__()
        self.element_gap = element_gap

    def on_draw(self, ctx):
        # we do this on draw because we want to make sure it is always drawn correctly
        # sometimes, objects are added after self.on_update ran, which would make them display wrong for one frame
        # if we put this into on_update instead
        #
        # we only inherit from GameObject so no super() call needed
        last_y = 0
        for g in self._game_objs:
            g.y = last_y # we can do this becasue objects of custom classes are passed by reference
            last_y += g.height + self.element_gap



class HPane(GameObject):
    def __init__(self, element_gap):
        super().__init__()
        self.element_gap = element_gap

    def on_draw(self, ctx):
        last_x = 0
        for g in self._game_objs:
            g.x = last_x # we can do this becasue objects of custom classes are passed by reference
            last_x += g.width + self.element_gap
