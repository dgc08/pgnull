import pygame

from .Clock import Clock
from .Keyboard import Keyboard
from .Screen import Screen

from . import utils

class Game:
    @staticmethod
    def get_game():
        if utils.glob_singleton.get("game"):
            return utils.glob_singleton["game"]
        else:
            return Game()

    def __init__(self, old_game=None):
        utils.glob_singleton["game"] = self
        if not old_game:
            pygame.init()
        else:
            self.screen = old_game.screen
        self.clock = Clock()
        self.keyboard = Keyboard()
        self.event_runner = utils.Game_Events()

        self.on_updates = []
        self.on_draws = []

        self.__running = False

    def open_screen(self, WIDTH, HEIGHT, caption="pgnull game"):
        self.screen = Screen(WIDTH, HEIGHT, caption)

    def run_game(self, run_object=None, update_fps=60, on_close=None):
        if callable(run_object):
            self.event_runner.on_update = run_object
        elif type(run_object) == utils.Game_Events:
            self.event_runner = run_object
        elif self.event_runner.on_update:
            pass
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
                elif event.type == pygame.KEYUP:
                    key = pygame.key.name(event.key).lower()
                    self.keyboard.set_key(key, False)

                    self.event_runner.on_key_up(event.key)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self.event_runner.on_mouse_down(mouse_pos, event.button)
                elif event.type == pygame.MOUSEBUTTONUP:
                    mouse_pos = pygame.mouse.get_pos()
                    self.event_runner.on_mouse_up(mouse_pos, event.button)
                elif event.type == pygame.MOUSEMOTION:
                    self.event_runner.on_mouse_move(event.pos, event.rel, event.buttons)
                elif event.type == pygame.QUIT:
                    self.event_runner.on_close()
                    self.close()
                self.clock.check_schedule(event.type)

            ctx = utils.Game_Context(events, self.keyboard)
            self.event_runner.on_update(ctx)
            for f in self.on_updates:
                f(ctx)

            self.event_runner.on_draw()
            for f in self.on_draws:
                f()

            pygame.display.update()
            self.clock.tick(update_fps)

        self.event_runner.on_close()
        
    def register_event(self, event: str, event_runnable):
        if not callable(event_runnable):
            raise TypeError("event_runnable isn't callable (It needs to be a reference to a function that can be executed)")

        if not hasattr(self.event_runner, event):
            event = "on_"+event
        if not hasattr(self.event_runner, event):
            raise TypeError("No Event named " + event)

        self.event_runner.__setattr__(event, event_runnable)
        return

    def event(self, event_name: str):
        def decorator(func):
            self.register_event(event_name, func)
            return func
        return decorator

    def close(self):
        pygame.quit()
        exit()

    def quit(self):
        self.__running = False
