from copy import deepcopy

import pygame

from pgnull.Clock import Clock
from pgnull.Screen import Screen

from pgnull.utils import *

class Game:
    def __init__(self):
        glob_singleton["game"] = self
        pygame.init()
        self.clock = Clock()
        self.keyboard = Keyboard()

        self.__running = False

    def open_screen(self, WIDTH, HEIGHT, caption="pgnull game"):
        self.screen = Screen(WIDTH, HEIGHT, caption)

    def run_game(self, update_function = keep_open, on_close = keep_open, update_fps = 60):
        self.__running = True
        score = 0
        while self.__running:
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.KEYDOWN:
                    key = pygame.key.name(event.key).lower()
                    self.keyboard.set_key(key, True)
                if event.type == pygame.KEYUP:
                    key = pygame.key.name(event.key).lower()
                    self.keyboard.set_key(key, False)
                if event.type == pygame.QUIT:
                    self.quit()

            update_function(Game_Context(events, self.keyboard))

            pygame.display.update()
            self.clock.tick(update_fps)

        on_close()
        self.__quit()

    def __quit(self):
        pygame.quit()
        exit()

    def quit(self):
        self.__running = False
