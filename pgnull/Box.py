#!/usr/bin/env python3

from pygame.rect import Rect
from pygame.math import Vector2
from pygame import draw
from pygame import MOUSEBUTTONDOWN
from pygame import mouse

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

    def on_draw(self):
        if self.color:
            draw.rect(Game.get_game().screen.pygame_obj, self.color, self)


class TextBox(Box):
    def __init__(self, text, pos:Vector2=None, size=None, color=None, topleft=None, fontsize=32, font=None, text_color=(0, 0, 0), font_kwargs={}, render_kwargs={}):
        if not topleft and not pos:
            raise Exception("No position argument passed")
        elif topleft:
            pos = (0,0)

        super().__init__(pos, size, color)

        self.box_topleft = topleft

        self.text = text
        self.text_color = text_color

        self.fontsize = fontsize
        self.font = font

        self.font_kwargs = font_kwargs
        self.render_kwargs = render_kwargs

    def on_draw(self):
        super().on_draw()
        
        screen = Game.get_game().screen

        if self.box_topleft:
            text_position = self.box_topleft
        else:
            text_width, text_height = screen.get_text_size(self.text, self.font, self.fontsize, self.font_kwargs)
            text_position = (self.left + (self.width - text_width) // 2, self.top + (self.height - text_height) // 2)

        screen.draw_text(self.text, text_position, self.font, self.fontsize, self.text_color, self.font_kwargs, self.render_kwargs)


class Button(TextBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_update(self, ctx):
        for event in ctx.events:
            if event.type == MOUSEBUTTONDOWN:
                pos = mouse.get_pos()
                button = event.button

                if button == 1 and self.collidepoint(pos):
                    self.on_click()

    @staticmethod
    def on_click():
        print("generic on click")
