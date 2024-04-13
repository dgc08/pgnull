from random import randint
import pgnull

game = pgnull.Game()

WIDTH = 400
HEIGHT = 400

game.open_screen(WIDTH, HEIGHT)

fox = pgnull.Actor("fox")
fox.pos = 100, 100

coin = pgnull.Actor("coin")
coin.pos = 200, 200

score = 0

def place_coin():
    coin.x = randint(20, (WIDTH-20))
    coin.y = randint(20, (HEIGHT-20))

def draw():
    game.screen.fill(pgnull.Colors.GREEN)
    game.screen.draw_text("Punkte: " + str(score), color="black", topleft=(10, 10))

    coin.draw()
    fox.draw()


def update(context):
    global score

    if context.keyboard.left:
        fox.x = fox.x - 2
    elif context.keyboard.right:
        fox.x = fox.x + 2
    if context.keyboard.up:
        fox.y = fox.y - 2
    elif context.keyboard.down:
        fox.y = fox.y + 2

    coin_collected = fox.colliderect(coin)
    if coin_collected:
        score += 10
        place_coin()

    if context.keyboard.j:
        game.quit()

    draw()

game.run_game(update)