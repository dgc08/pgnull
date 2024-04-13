import pygame.time as pgtime

class Clock:
    def __init__(self):
        self.pygame_obj = pgtime.Clock()
        self.tick = self.pygame_obj.tick