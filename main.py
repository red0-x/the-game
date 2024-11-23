import pygame
import sys
import json

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
gross_elevation = 1000
# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Sprite Example")
idle4 = pygame.image.load("images/player/idle/sprite_0.png")
idle4_ = pygame.image.load("images/player/idle/sprite_1.png")
bg1 = pygame.transform.scale_by(pygame.image.load("images/background/01background.png"), 2).convert()

bg2 = pygame.image.load("images/background/02background.png").convert()
bg3 = pygame.image.load("images/background/03background.png").convert()
# Define a color
WHITE = (255, 255, 255)


# Create a Sprite class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Load an image or create a surface
        self.image = pygame.image.load("images/player/idle/idle-04.png")

        # Set a rect for positioning
        self.rect = self.image.get_rect()
        self.rect.center = (player_start[0][0], player_start[0][1])
        self.y_vel = 0
        self.x_vel = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if self.x_vel > 0:
            self.image = idle4
        elif self.x_vel < 0:
            self.image = idle4_

        
        self.y_vel += 2
        if abs(self.x_vel) > 1.5:
            self.x_vel += self.x_vel * -0.10
        elif abs(self.x_vel) < 0.51:
            self.x_vel = 0
        elif self.x_vel < 1.5 and self.x_vel > 0.51:
            self.x_vel -= 0.5
        elif self.x_vel > -1.5 and self.x_vel < 0.51:
            self.x_vel += 0.5

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x_vel-= 0.75
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x_vel += 0.75

        # Move the player rect
        self.rect.x += self.x_vel
        if pygame.sprite.spritecollide(self, blocks_list, False):
            # Undo movement if collision occurs
            self.rect.x -= self.x_vel
            self.x_vel = 0

        
        self.on_ground = False
        self.rect.y += self.y_vel
        if pygame.sprite.spritecollide(self, blocks_list, False):
            # Undo movement if collision occurs
            self.rect.y -= self.y_vel
            if self.y_vel > 0:
                self.on_ground = True
            self.y_vel = 0
            
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
player_start = [(320, 0), (250, -200), (600, 300)]
level = 0
blocks_list = []
block_types = [
    Block1,
]

# map = maps[0]
# for r, row in enumerate(map):
#     for c, block in enumerate(row):
#         if block != 0:
#             blocks_list.append(block_types[block - 1](c * 32 + 16, r * 32 + 16))

player = Player()
all_sprites.add(player)

def change_level(level_num):
    blocks_list.clear()
    all_sprites.empty()
    player.y_vel = 0
    player.x_vel = 0
    all_sprites.add(player)
    player.rect.x = player_start[level][0]
    player.rect.y = player_start[level][1]
    map = maps[level_num]
    for r, row in enumerate(map):
        for c, block in enumerate(row):
            if block != 0:
                blocks_list.append(block_types[block - 1](c * 32 + 16, r * 32 + 16))
    for block in blocks_list:
        all_sprites.add(block)
change_level(0)

# Main game loop
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update sprites
    all_sprites.update()

    if player.rect.y > 900:
        level += 1
        change_level(level)
        gross_elevation -= 50
    # Draw everything
    screen.fill(WHITE)  # Clear the screen
    screen.blit(bg1, (0, 0))
    all_sprites.draw(screen)

    # Flip the display
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(60)

pygame.quit()
sys.exit()
