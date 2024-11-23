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
        self.image = pygame.image.load("images/idle-04.png").convert()

        # Set a rect for positioning
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.y_vel = 0

    def update(self):
        keys = pygame.key.get_pressed()
        move_x = 0
        
        self.y_vel += 2
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            move_x = - 5
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            move_x = 5
        # if keys[pygame.K_UP] or keys[pygame.K_W]:
        #     move_y = - 5
        # if keys[pygame.K_DOWN] or keys[pygame.K_S]:
        #     move_y = 5

        # Move the player rect
        self.rect.x += move_x
        if pygame.sprite.spritecollide(self, blocks_list, False):
            # Undo movement if collision occurs
            self.rect.x -= move_x
        
        self.on_ground = False
        self.rect.y += self.y_vel
        if pygame.sprite.spritecollide(self, blocks_list, False):
            # Undo movement if collision occurs
            self.rect.y -= self.y_vel
            if self.y_vel > 0:
                self.y_vel = 0
                self.on_ground = True
            
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.y_vel = -20

next_id = 1
class Block1(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Load an image or create a surface
        self.image = pygame.image.load("images/tile1.png").convert()

        # Set a rect for positioning
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        global next_id
        self.id_num = next_id
        next_id += 1


# Create a sprite group and add the player
all_sprites = pygame.sprite.Group()

blocks_list = [
    Block1(100, 100),
    Block1(100, 500),
    Block1(400, 500),
]
player = Player()
all_sprites.add(player)
for block in blocks_list:
    all_sprites.add(block)


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
