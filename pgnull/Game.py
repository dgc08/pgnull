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

    def __init__(self, WIDTH=None, HEIGHT=None, caption="pgnull game"):
        if WIDTH:
            self.init_screen(WIDTH, HEIGHT, caption)
        else:
            self.pygame_available = False

        utils.glob_singleton["game"] = self

        self.__running = False

    def init_screen(self, WIDTH, HEIGHT, caption="pgnull game", *args, **kwargs):
        self.pygame_available = True
        pygame.init()

        self.screen = Screen(WIDTH, HEIGHT, caption, *args, **kwargs)
        self.clock = Clock()
        self.keyboard = Keyboard()


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
            if not self.scene:
                # return back to the caller of run_game
                return

            if self.pygame_available:
                events = pygame.event.get()

                ctx = utils.Game_Context(events, self.keyboard)
                ctx.mouse_rel = pygame.mouse.get_rel()

                for event in events:
                    if event.type == pygame.KEYDOWN:
                        key = pygame.key.name(event.key).lower()
                        self.keyboard.set_key(key, True)
                        ctx.event_args["on_key_down"] = (event.key, )
                    elif event.type == pygame.KEYUP:
                        key = pygame.key.name(event.key).lower()
                        self.keyboard.set_key(key, False)
                        ctx.event_args["on_key_up"] = (event.key, )
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        ctx.event_args["on_mouse_down"] = (mouse_pos, event.button)
                    elif event.type == pygame.MOUSEBUTTONUP:
                        mouse_pos = pygame.mouse.get_pos()
                        ctx.event_args["on_mouse_up"] = (mouse_pos, event.button)
                    elif event.type == pygame.MOUSEMOTION:
                        ctx.event_args["on_mouse_move"] = (event.pos, event.rel, event.buttons)
                    elif event.type == pygame.QUIT:
                        ctx.event_args["on_close"] = ()
                        self.__running = False
                    self.clock.check_schedule(event.type)
            else: # we somehow use this framework without pygame
                ctx = utils.Game_Context(None, None)

            self.scene.do_update(ctx)
            if not self.scene:
                # sometimes, update kills the scene
                return 
            self.scene.do_draw(ctx)

            if self.pygame_available:
                pygame.display.update()
                self.clock.tick(update_fps)

        self.scene.on_close()
        self.close()

    def close(self):
        if self.pygame_available:
            pygame.quit()
        self.pygame_available = False
        exit()

    def quit(self):
        self.__running = False
    def dequeue(self):
        # alias for quit, in case some Scene wants to dequeue their parent and the parent is the game
        self.quit()

    def perform_dequeue_for(self, obj):
        if self.scene == obj:
            self.scene = None
