import pygame.image
from pygame.sprite import Sprite

from pgnull.utils import glob_singleton

class Actor(Sprite):
    def __init__(self, name):
        super(Actor, self).__init__()
        self.pygame_obj = self
        path = "images/" + name + ".png"
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect()

        self.colliderect = self.rect.colliderect

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

    def draw(self):
        glob_singleton["game"].screen.blit(self.image, self.rect)

