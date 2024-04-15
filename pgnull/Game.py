import pygame

from pgnull.Clock import Clock
from pgnull.Keyboard import Keyboard
from pgnull.Screen import Screen

import pgnull.utils

class Game:
    def __init__(self):
        pgnull.utils.glob_singleton["game"] = self
        pygame.init()
        self.clock = Clock()
        self.keyboard = Keyboard()
        self.event_runner = pgnull.utils.Game_Events()

        self.__running = False

    def open_screen(self, WIDTH, HEIGHT, caption="pgnull game"):
        self.screen = Screen(WIDTH, HEIGHT, caption)

    def run_game(self, run_object=None, update_fps=60, on_close=None):
        if callable(run_object):
            self.event_runner.on_update = run_object
        elif type(run_object) == pgnull.utils.Game_Events:
            self.event_runner = run_object
        else:
            raise TypeError("run_object isn't callable or an instance of Game_Events (It can either be a reference to an update function or a pgnull.Game_Events with all the relevant functions implemented)")

        if callable(on_close):
            self.event_runner.on_close = on_close

        self.__run_game_loop(update_fps)

    def __run_game_loop(self, update_fps):
        self.__running = True
        while self.__running:
            self.event_runner.on_iteration_start()
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.KEYDOWN:
                    key = pygame.key.name(event.key).lower()
                    self.keyboard.set_key(key, True)

                    self.event_runner.on_key_down(event.key)
                if event.type == pygame.KEYUP:
                    key = pygame.key.name(event.key).lower()
                    self.keyboard.set_key(key, False)

                    self.event_runner.on_key_up(event.key)
                if event.type == pygame.QUIT:
                    self.quit()
                self.clock.check_schedule(event.type)

            self.event_runner.on_update(pgnull.utils.Game_Context(events, self.keyboard))

            self.event_runner.on_draw()
            pygame.display.update()
            self.clock.tick(update_fps)

        self.event_runner.on_close()
        self.__quit()

    def register_event(self, event: str, event_runnable):
        if not callable(event_runnable):
            raise TypeError("event_runnable isn't callable (It needs to be a reference to a function that can be executed)")

        if event == "on_close":
            self.event_runner.on_close = event_runnable
        elif event == "on_iteration_start":
            self.event_runner.on_iteration_start = event_runnable

    def __quit(self):
        pygame.quit()
        exit()

    def quit(self):
        self.__running = False
