import pygame
import sys
import asyncio
import os

# Initialize Pygame
pygame.init()

# Constants
FPS = 60
BACKGROUND_COLOR = (0, 0, 0)  # Black background

# Initialize screen
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pygame Game Template")
image = pygame.image.load("images/placeholder.png").convert()

# Clock to control frame rate
clock = pygame.time.Clock()

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Define a basic player object
player = pygame.Rect(800 // 2, 600 // 2, 50, 50)  # A rectangle representing the player
player_speed = 5  # Movement speed
def handle_input(keys, player, player_speed):
    
    #ARROW KEYS

    if keys[pygame.K_UP]:
        player.y -= player_speed
    if keys[pygame.K_DOWN]:
        player.y += player_speed
    if keys[pygame.K_LEFT]:
        player.x -= player_speed
    
    #WASD

    if keys[pygame.K_d]:
        player.x += player_speed
    if keys[pygame.K_w]:
        player.y -= player_speed
    if keys[pygame.K_s]:
        player.y += player_speed
    if keys[pygame.K_a]:
        player.x -= player_speed



async def main():
    """Main game loop."""
    if os.environ.get("PYGBAG"):
        print("Running in Pygbag")
        await asyncio.sleep(1)  # Allow browser to initialize

    running = True
    while running:
        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Quit event
                running = False

        # Input Handling
        keys = pygame.key.get_pressed()
        handle_input(keys, player, player_speed)

        # Rendering
        screen.fill(BACKGROUND_COLOR)  # Clear the screen with background color
        #pygame.draw.rect(screen, RED, player)  # Draw the player
        screen.blit(image, (player))
        pygame.display.flip()  # Update the display
        await asyncio.sleep(0)  # Very important for async
        # Maintain frame rate
        clock.tick(FPS)


asyncio.run(main())
