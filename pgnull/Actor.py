import pygame.image
from pygame.sprite import Sprite

from pgnull.utils import glob_singleton

class Actor(Sprite):
    def __init__(self, name):
        super(Actor, self).__init__()
        self.pygame_obj = self
        path = "images/" + name + ".png"
        self.original_image = pygame.image.load(path)
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.scale(1, 1)
        self.rotate(45)

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

    def scale(self, x, y):
        self.scale_val = (x,y)
        original_width, original_height = self.original_image.get_size()

        new_width = int(original_width * x)
        new_height = int(original_height * y)

        self.image = pygame.transform.scale(self.image, (new_width, new_height))
        self.rect = self.image.get_rect(center=self.rect.center)
        self.colliderect = self.rect.colliderect

    def rotate(self, angle):
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.scale(*self.scale_val)

    def draw(self):
        glob_singleton["game"].screen.blit(self.image, self.rect)

