from pygame import display
import pygame.font

from pygame import draw

class Screen:
    def __init__(self, WIDTH, HEIGHT, caption):
        self.pygame_obj = display.set_mode((WIDTH, HEIGHT))
        display.set_caption(caption)

        self.fill = self.pygame_obj.fill
        self.blit = self.pygame_obj.blit
        self.surface = self.pygame_obj

        self.draw = draw

    def draw_text(self, text , topleft, font=None, fontsize = 32, color=(0,0,0), font_kwargs={}, render_kwargs={}):
        font = pygame.font.Font(font, fontsize, **font_kwargs)
        text_obj = font.render(text, True, color, **render_kwargs)
        self.blit(text_obj, topleft)

    def get_text_size(self, text, font=None, fontsize=32, line_gap = 3, font_kwargs={}):
        font = pygame.font.Font(font, fontsize, **font_kwargs)
        lines = text.split('\n')
        widths, heights = zip(*(font.render(line, True, (0, 0, 0)).get_size() for line in lines))
        total_height = sum(heights)
        max_width = max(widths)
        return max_width, total_height

    def draw_textbox(self, text, rect, font=None, fontsize=32, color=(0, 0, 0),
                     font_kwargs={}, render_kwargs={}):
        text_width, text_height = self.get_text_size(text, font, fontsize, font_kwargs)
        text_position = (rect.left + (rect.width - text_width) // 2, rect.top + (rect.height - text_height) // 2)
        self.draw_text(text, text_position, font, fontsize, color, font_kwargs, render_kwargs)
