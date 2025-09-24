import pygame

from pygame.math import Vector2
from .GameObject import GameObject
from .Game import Game

# made with chatgpt in analogy to Box
class Circle(GameObject):
    def __init__(self, pos: Vector2, radius: int = 0, color=None, outline=0):
        self.color = color
        self.outline = outline
        self.pos = Vector2(pos)
        self.radius = radius

        GameObject.__init__(self)

    def collidepoint(self, point: tuple[int, int]) -> bool:
        """Check if a point lies within the circle."""
        return self.pos.distance_to(Vector2(point)) <= self.radius

    def on_draw(self, ctx):
        if self.color:
            pygame.draw.circle(
                Game.get_game().screen.pygame_obj,
                self.color,
                self.pos,
                self.radius,
                self.outline
            )

        for event in ctx.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                button = event.button

                if button == 1 and self.collidepoint(pos):
                    self.on_click()

    def on_click(self):
        pass
