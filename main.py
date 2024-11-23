import pygame
import sys
import json

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Sprite Example")
idle4 = pygame.image.load("images/player/idle/idle-04.png").convert()
idle4_ = pygame.transform.flip(idle4, True, False)
# Define a color
WHITE = (255, 255, 255)


# Create a Sprite class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Load an image or create a surface
        self.image = pygame.image.load("images/player/idle/idle-04.png").convert()

        # Set a rect for positioning
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.y_vel = 0
        self.x_vel = 0

    def update(self):
        keys = pygame.key.get_pressed()
        move_x = 0
        if self.x_vel > 0:
            self.image = idle4
        elif self.x_vel < 0:
            self.image = idle4_

        
        self.y_vel += 2
        if abs(self.x_vel) > 1.5:
            self.x_vel += self.x_vel * -0.10
        elif abs(self.x_vel) < 0.51:
            self.x_vel = 0
        elif self.x_vel < 1.5 and self.x_vel > 0:
            self.x_vel -= 0.5
        elif self.x_vel > -1.5 and self.x_vel < 0:
            self.x_vel += 0.5

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x_vel-= 0.75
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x_vel += 0.75
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
        self.rect.x += self.x_vel
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
    image = pygame.image.load("images/tile1.png").convert()
    def __init__(self, x, y):
        super().__init__()

        # Set a rect for positioning
        self.rect = self.image.get_rect()
        self.rect.inflate_ip(-10, -10)
        self.rect.center = (x, y)
        global next_id
        self.id_num = next_id
        next_id += 1


# Create a sprite group and add the player
all_sprites = pygame.sprite.Group()


with open("map.json") as file:
    maps = json.load(file)

blocks_list = []
block_types = [
    Block1,
]

map = maps[0]
for r, row in enumerate(map):
    for c, block in enumerate(row):
        if block != 0:
            blocks_list.append(block_types[block - 1](c * 32 + 16, r * 32 + 16))
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
