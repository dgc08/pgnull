from pygame import display
import pygame.font
from pgnull.utils import Colors

class Screen:
    def __init__(self, WIDTH, HEIGHT, caption):
        self.pygame_obj = display.set_mode((WIDTH, HEIGHT))
        display.set_caption(caption)

        self.fill = self.pygame_obj.fill
        self.blit = self.pygame_obj.blit

    def draw_text(self, text , topleft, font=None, fontsize = 32, color=Colors.BLACK, font_kwargs={}, render_kwargs={}):
        font = pygame.font.Font(font, fontsize, **font_kwargs)
        text_obj = font.render(text, True, color, **render_kwargs)
        self.blit(text_obj, topleft)