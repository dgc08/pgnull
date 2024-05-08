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

    def draw_rect(self, rect, color):
        pygame.draw.rect(self.pygame_obj, color, rect)

    def get_text_size(self, text, font=None, fontsize=32, font_kwargs={}):
        font = pygame.font.Font(font, fontsize, **font_kwargs)
        text_surface = font.render(text, True, (0, 0, 0))
        return text_surface.get_size()

    def draw_textbox(self, text, rect, font=None, fontsize=32, color=(0, 0, 0),
                     font_kwargs={}, render_kwargs={}):
        text_width, text_height = self.get_text_size(text, font, fontsize, font_kwargs)
        text_position = (rect.left + (rect.width - text_width) // 2, rect.top + (rect.height - text_height) // 2)
        self.draw_text(text, text_position, font, fontsize, color, font_kwargs, render_kwargs)
