import pygame
import random

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
PINK = (255, 192, 203)

# Define screen dimensions
WIDTH = 400
HEIGHT = 400

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fox and Coin")
clock = pygame.time.Clock()


# Load images (replace "fox.png" and "coin.png" with your image paths)
fox_image = pygame.image.load("images/fox.png")
coin_image = pygame.image.load("images/coin.png")

# Define object classes (optional for better organization)
class Fox(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 100

class Coin(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()

# Create fox and coin objects
fox = Fox(fox_image)
coin = Coin(coin_image)

# Game variables
score = 0
game_over = False

# Function to place the coin at a random position
def place_coin():
    coin.rect.x = random.randint(20, WIDTH - coin.rect.width - 20)
    coin.rect.y = random.randint(20, HEIGHT - coin.rect.height - 20)

# Function for game over screen
def game_over_screen():
    screen.fill(PINK)
    font = pygame.font.Font(None, 60)
    text = font.render("Endstand: " + str(score), True, BLACK)
    screen.blit(text, (10, 10))
    font = pygame.font.Font(None, 40)
    text = font.render("Noch mal spielen? (j/n)", True, BLACK)
    screen.blit(text, (10, 100))


# Main game loop
running = True
timer = pygame.time.get_ticks()
while running:
    ticks = pygame.time.get_ticks() - timer
    timer = pygame.time.get_ticks()
    if timer > 15 * 1000:
        game_over = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_j:
                game_over = False
                score = 0
                # Schedule time up event (optional)
                # pygame.time.set_timer(pygame.USEREVENT, 15000)  # 15 seconds
            elif event.key == pygame.K_n:
                running = False

    # Handle keyboard input (movement)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        fox.rect.x -= 2
    elif keys[pygame.K_RIGHT]:
        fox.rect.x += 2
    elif keys[pygame.K_UP]:
        fox.rect.y -= 2
    elif keys[pygame.K_DOWN]:
        fox.rect.y += 2

    # Check for collision with coin
    if fox.rect.colliderect(coin):
        score += 10
        place_coin()

    # Fill screen with green
    screen.fill(GREEN)

    # Draw fox and coin
    screen.blit(fox.image, fox.rect)
    screen.blit(coin.image, coin.rect)

    # Draw score text
    font = pygame.font.Font(None, 32)
    text = font.render("Punkte: " + str(score), True, BLACK)
    screen.blit(text, (10, 10))

    # Draw game over screen if game over
    if game_over:
        game_over_screen()

        # Update the display
    pygame.display.flip()

    # Set frame rate
    clock.tick(60)

# Quit pygame
pygame.quit()