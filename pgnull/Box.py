#!/usr/bin/env python3

from pygame.rect import Rect
from pygame.math import Vector2
from pygame import draw
from pygame import MOUSEBUTTONDOWN
from pygame import mouse
from pygame import font as font_pg

#import pygame

from .Game import Game
from .GameObject import GameObject

class Box(GameObject, Rect):
    def __init__(self, pos:Vector2, size:Vector2=None, color=None):
        self.color = color

        GameObject.__init__(self)

        if size:
            Rect.__init__(self, *pos, *size)
        else:
            Rect.__init__(self, pos, (0,0))

    @property
    def pos(self) -> Vector2:
        return Vector2(self.x, self.y)
    @pos.setter
    def pos(self, value: Vector2):
        self.x, self.y = value

    def on_draw(self, ctx):
        if self.color:
            draw.rect(Game.get_game().screen.pygame_obj, self.color, self)


class TextBox(GameObject):
    def __init__(self, text, pos:Vector2=None, size=None, color=None, topleft=None, fontsize=32, font=None, line_gap=3, text_color=(0, 0, 0), font_kwargs={}, render_kwargs={}):
        if not topleft and not pos:
            raise Exception("No position argument passed")
        elif topleft:
            self.box = Box((0,0), size, color)
            self.box_topleft = Vector2(topleft)
            self.box.topleft = self.box_topleft
            pos = Vector2(0,0)
            super().__init__()
        else:
            self.box = Box(pos, size, color)
            self.box_topleft = None
            super().__init__() # because this resets the position
            self.pos = pos
        
        self.text = text
        self.text_color = text_color

        self.fontsize = fontsize
        self.font = font
        self.line_gap = line_gap

        self.font_kwargs = font_kwargs
        self.render_kwargs = render_kwargs

    def get_text_size(self):
        return Game.get_game().screen.get_text_size(self.text, self.font, self.fontsize, self.line_gap, self.font_kwargs)

    @property
    def width(self):
        return self.get_text_size()[0]
    @width.setter
    def width(self, val):
        pass

    @property
    def pos(self):
        return self.box.pos
    @pos.setter
    def pos(self, val):
        if self.box_topleft:
            self.box_topleft += Vector2(val)-self.pos
        else:
            self.box.pos = Vector2(val)

    @property
    def height(self):
        return self.get_text_size()[1]
    @height.setter
    def height(self, val):
        pass


    def on_draw(self, ctx):
        super().on_draw(ctx)

        screen = Game.get_game().screen

        text_width, text_height = screen.get_text_size(self.text, self.font, self.fontsize, self.font_kwargs)

        if self.box_topleft:
            x, y = self.box_topleft
        else:
            x = self.box.left + (self.box.width - text_width) // 2
            y = self.box.top + (self.box.height - text_height) // 2

        font = font_pg.Font(self.font, self.fontsize, **self.font_kwargs)
        lines = self.text.split('\n')

        for line in lines:
            text_surface = font.render(line, True, self.text_color)
            screen.surface.blit(text_surface, (x, y))
            y += text_surface.get_height() + self.line_gap
