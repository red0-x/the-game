import pygame
import sys
import asyncio
import os
import input_

# Initialize Pygame
pygame.init()

# Constants
FPS = 60
BACKGROUND_COLOR = (0, 0, 0)  # Black background

# Initialize screen
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pygame Game Template")
image = pygame.image.load("images/robotDrawing.png").convert()

# Clock to control frame rate
clock = pygame.time.Clock()

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Define a basic player object
player = pygame.Rect(800 // 2, 600 // 2, 50, 50)  # A rectangle representing the player
player_speed = 5  # Movement speed


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
        input_.handle_input(keys, player, player_speed)

        # Rendering
        screen.fill(BACKGROUND_COLOR)  # Clear the screen with background color
        #pygame.draw.rect(screen, RED, player)  # Draw the player
        screen.blit(image, (player))
        pygame.display.flip()  # Update the display
        await asyncio.sleep(0)  # Very important for async
        # Maintain frame rate
        clock.tick(FPS)


asyncio.run(main())
