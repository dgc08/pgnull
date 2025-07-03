from pygame import display
import pygame.font

from pygame import draw

# Alte klasse aus der zeit wenn alles in analogie zu pgzero gemacht wurde, man könnte diese Funktionen auch direkt in class Game tun
# TODO
class Screen:
    def __init__(self, WIDTH, HEIGHT, caption):
        self.pygame_obj = display.set_mode((WIDTH, HEIGHT))
        display.set_caption(caption)

        self.fill = self.pygame_obj.fill
        self.blit = self.pygame_obj.blit
        self.surface = self.pygame_obj

        self.draw = draw

    def get_text_size(self, text, font=None, fontsize=32, line_gap = 3, font_kwargs={}):
        # chatgpt
        lines = text.split('\n')
        widths, heights = zip(*(font.render(line, True, (0, 0, 0)).get_size() for line in lines))
        total_height = sum(heights)
        max_width = max(widths)
        return max_width, total_height
