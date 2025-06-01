import pygame

from .Clock import Clock
from .Keyboard import Keyboard
from .Screen import Screen

from . import utils

class Game:
    game = None
    @staticmethod
    def get_game():
        if utils.glob_singleton.get("game"):
            return utils.glob_singleton["game"]
        else:
            return Game()

    def __init__(self, WIDTH, HEIGHT, caption="pgnull game"):
        utils.glob_singleton["game"] = self

        pygame.init()
        self.screen = Screen(WIDTH, HEIGHT, caption)
        self.clock = Clock()
        self.keyboard = Keyboard()

        self.__running = False

    def load_scene(self, scene):
        scene.parent = self
        self.scene = scene
        scene.on_start()

    def run_game(self, scene=None, update_fps=60):
        if scene:
            self.load_scene(scene)
        self.__run_game_loop(update_fps)

    def __run_game_loop(self, update_fps):
        self.__running = True
        while self.__running:
            self.scene.on_iteration_start()
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.KEYDOWN:
                    key = pygame.key.name(event.key).lower()
                    self.keyboard.set_key(key, True)

                    self.scene.on_key_down(event.key)
                elif event.type == pygame.KEYUP:
                    key = pygame.key.name(event.key).lower()
                    self.keyboard.set_key(key, False)

                    self.scene.on_key_up(event.key)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self.scene.on_mouse_down(mouse_pos, event.button)
                elif event.type == pygame.MOUSEBUTTONUP:
                    mouse_pos = pygame.mouse.get_pos()
                    self.scene.on_mouse_up(mouse_pos, event.button)
                elif event.type == pygame.MOUSEMOTION:
                    self.scene.on_mouse_move(event.pos, event.rel, event.buttons)
                elif event.type == pygame.QUIT:
                    self.scene.on_close()
                    self.close()
                self.clock.check_schedule(event.type)

            ctx = utils.Game_Context(events, self.keyboard)

            self.scene.do_update(ctx)
            self.scene.do_draw()

            pygame.display.update()
            self.clock.tick(update_fps)

        self.scene.on_close()
        self.close()

    def close(self):
        pygame.quit()
        exit()

    def quit(self):
        self.__running = False
    def dequeue(self):
        # alias for quit, in case some Scene wants to dequeue their parent and the parent is the game
        self.quit()
