#!/usr/bin/env python3

from pygame.rect import Rect

from .Game import Game
from .GameObject import GameObject

class Box(GameObject, Rect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
