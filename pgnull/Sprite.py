import pygame.image
from pygame.sprite import Sprite as pygame_sprite
from pygame.math import *

from .utils import glob_singleton

class Sprite(pygame_sprite):
    def __init__(self, image_path, pos=None, scale=(1,1), angle=0):
        super(Sprite, self).__init__()
        self.pygame_obj = self
        self.original_image = pygame.image.load(image_path)
        self.image = self.original_image
        self.rect = self.image.get_rect()

        self.__scale_val = Vector2(scale)
        self.__angle = angle
        self.scale = scale
        self.rotation = angle

        if pos:
            self.pos = pos
            print("set to ", pos)

    @property
    def pos(self):
        return self.rect.x, self.rect.y

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

    @pos.setter
    def pos(self, value):
        self.rect.x, self.rect.y = value

    def __rescale_and_rotate(self):
        #prev_img = self.image

        original_width, original_height = self.original_image.get_size()

        new_width = int(original_width * self.__scale_val[0])
        new_height = int(original_height * self.__scale_val[1])

        self.image = pygame.transform.rotate(
            pygame.transform.scale(self.original_image, (new_width, new_height)),
            self.__angle
        )
        self.rect = self.image.get_rect(center=self.rect.center)

        #self.image = pygame.transform.scale(self.image, (new_width, new_height))
        #self.rect = self.image.get_rect(center=self.rect.center)
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
        value = value % 360
        self.__angle = value
        self.__rescale_and_rotate()


    def draw(self):
        glob_singleton["game"].screen.blit(self.image, self.rect)

