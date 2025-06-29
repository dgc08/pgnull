import pygame
from .GameObject import GameObject
from .Game import Game

class AudioPlayer(GameObject):
    def __init__(self, file_path=None):
        super().__init__()
        self.channel = None
        pygame.mixer.init()
        self.sound = pygame.mixer.Sound(file_path) if file_path else None

    def load(self, file_path):
        self.sound = pygame.mixer.Sound(file_path)

    def play(self, loops=0):
        if self.sound:
            self.channel = self.sound.play(loops=loops)

    def stop(self):
        if self.channel and Game.get_game().pygame_available:
            self.channel.stop()

    def set_volume(self, volume):
        if self.sound:
            self.sound.set_volume(volume)

    def is_playing(self):
        return self.channel.get_busy() if self.channel else False

    def __del__(self):
        self.stop()
