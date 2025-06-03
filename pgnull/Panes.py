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
        for g in self.get_children():
            g.pos = (g.pos[0], last_y) # we can do this becasue objects of custom classes are passed by reference
            last_y += g.height + self.element_gap

    @property
    def height(self):
        ret = 0
        for g in self.get_children():
            ret += g.height + self.element_gap

        if ret == 0:
            return 0

        return ret - self.element_gap
    @height.setter
    def height(self, v):
        pass #discard

    @property
    def width(self):
        ret = 0
        for g in self.get_children():
            if g.width > ret:
                ret = g.width
        return ret
    @width.setter
    def width(self, v):
        pass #discard



class HPane(GameObject):
    def __init__(self, element_gap):
        super().__init__()
        self.element_gap = element_gap

    def on_draw(self, ctx):
        last_x = 0
        for g in self.get_children():
            g.pos = (last_x, g.pos[1]) # we can do this becasue objects of custom classes are passed by reference
            last_x += g.width + self.element_gap

    @property
    def width(self):
        ret = 0
        for g in self.get_children():
            ret += g.width + self.element_gap

        if ret == 0:
            return 0

        return ret - self.element_gap
    @width.setter
    def width(self, v):
        pass #discard

    @property
    def height(self):
        ret = 0
        for g in self.get_children():
            if g.height > ret:
                ret = g.height
        return ret
    @height.setter
    def height(self, v):
        pass #discard
