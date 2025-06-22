import pygame.image
from pygame.sprite import Sprite as pygame_sprite
from pygame import MOUSEBUTTONDOWN
from pygame import mouse
from pygame.math import *

from .Game import Game
from .GameObject import GameObject

class Sprite(GameObject, pygame_sprite):
    def __init__(self, image_path, pos=None, scale=(1,1), angle=0, pivot=(0,0)):

        # load image and rect before super().__init__, because GameObject.__init__() sets the position to zero,
        # which links back to self.rect and causes an AttributeError otherwise
        self.original_image = pygame.image.load(image_path)
        self.image = self.original_image
        self.rect = self.image.get_rect()

        super(Sprite, self).__init__()

        scale = Vector2(scale)
        
        self.__scale_val = Vector2(scale)
        self.__angle = angle
        self.scale = scale
        self.rotation = angle

        if pos:
            self.pos = Vector2(pos)

    @property
    def pos(self):
        return Vector2(self.rect.x, self.rect.y)
    @pos.setter
    def pos(self, value):
        self.rect.x, self.rect.y = value

    @property
    def x(self):
        return self.rect.x
    @x.setter
    def x(self, value):
        self.rect.x = value

    @property
    def y(self):
        return self.rect.y
    @y.setter
    def y(self, value):
        self.rect.y = value

    @property
    def height(self):
        return self.rect.height
    @property
    def width(self):
        return self.rect.width

    def __rescale_and_rotate(self):
        # prev_img = self.image
        # diese funktion hat chatgpt code

        original_width, original_height = self.original_image.get_size()

        new_width = int(original_width * self.__scale_val[0])
        new_height = int(original_height * self.__scale_val[1])

        self.image = pygame.transform.rotate(
            pygame.transform.scale(self.original_image, (new_width, new_height)),
            self.__angle
        )
        self.rect = self.image.get_rect(center=self.rect.center)

        self.colliderect = self.rect.colliderect

    def set_size(self, x, y):
        # nicht scale setzen, (also 1x vergrößert, 2x vergrößert etc) sondern die direkte größe in pixel
        # dies ist natürlich einfacher wie scale
        self.image = pygame.transform.rotate(
            pygame.transform.scale(self.original_image, (x, y)),
            self.__angle
        )
        self.rect = self.image.get_rect(center=self.rect.center)

        self.colliderect = self.rect.colliderect

    @property
    def scale(self):
        return self.__scale_val
    @scale.setter
    def scale(self, value):
        self.__scale_val = Vector2(value)
        self.__rescale_and_rotate()

    @property
    def rotation(self):
        return self.__angle
    @rotation.setter
    def rotation(self, value):
        value = value % 360.0
        self.__angle = value
        self.__rescale_and_rotate()

    @property
    def center(self):
        return self.rect.center
    @center.setter
    def center(self, value):
        self.rect.center = value

    def on_draw(self, ctx):
        # check for click in on_draw, to get offseted position (= actual position on screen) for click checking
        self.check_for_click(ctx)

        Game.get_game().screen.blit(self.image, self.rect)

    def check_for_click(self, ctx):
        for event in ctx.events:
            # dies wurde größtenteils von irgendwo her kopiert aber ich weiß nicht von wo
            if event.type == MOUSEBUTTONDOWN:
                pos = mouse.get_pos()
                button = event.button

                if button == 1 and self.rect.collidepoint(pos):
                    self.on_click()

    def on_click(self):
        pass
