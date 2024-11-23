import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Sprite Example")

# Define a color
WHITE = (255, 255, 255)


# Create a Sprite class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Load an image or create a surface
        self.image = pygame.image.load("images/placeholder.png").convert()

        # Set a rect for positioning
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    def update(self):
        # Move the sprite with arrow keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        if keys[pygame.K_UP]:
            self.rect.y -= 5
        if keys[pygame.K_DOWN]:
            self.rect.y += 5

class Block1(pygame.sprite.Sprite):
    def __init__(self, id_num, x, y):
        super().__init__()
        # Load an image or create a surface
        self.image = pygame.image.load("images/tile1.png").convert()

        # Set a rect for positioning
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.id_num = id_num


# Create a sprite group and add the player
all_sprites = pygame.sprite.Group()
player = Player()
blocks_lists_x = [100, 200]
blocks_lists_y = [100, 500]
blocks_list = []
for i in range(len(blocks_lists_x)):
    blocks_list.append(Block1(i, blocks_lists_x[i], blocks_lists_y[i]))
all_sprites.add(player)
for i in range(len(blocks_list)):
    all_sprites.add(blocks_list[i])


# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update sprites
    all_sprites.update()

    # Draw everything
    screen.fill(WHITE)  # Clear the screen
    all_sprites.draw(screen)  # Draw sprites onto the screen

    # Flip the display
    pygame.display.flip()

    # Limit the frame rate
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
