from .Game import Game

class GameObject:
    def __init__(self):
        self.active = True

        Game.get_game().on_draws.append(self.__draw)
        Game.get_game().on_updates.append(self.__update)

    # Dequeue so it's functions won't get called
    def dequeue(self):
        game = Game.get_game()
        if self.draw in game.on_draws:
            game.on_draws.remove(self.draw)
        self.active = False

    def __draw(self):
        if self.active:
            self.draw()

    def __update(self, ctx):
        if self.active:
            self.update(ctx)

    def draw(self, ):
        pass
    def update(self, ctx):
        pass
