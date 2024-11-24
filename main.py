import pygame
import sys
import json

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
gross_elevation = 1000
free_falling = False
# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Sprite Example")
idle4 = pygame.image.load("images/player/idle/sprite_0.png")
idle4_ = pygame.image.load("images/player/idle/sprite_1.png")
bg1 = pygame.transform.scale_by(pygame.image.load("images/background/01background.png"), 2).convert_alpha()
bg2 = pygame.transform.scale_by(pygame.image.load("images/background/02background.png"), 2).convert_alpha()
bg3 = pygame.transform.scale_by(pygame.image.load("images/background/03background.png"), 2).convert_alpha()
rect1 = idle4.get_rect()
rect2 = idle4_.get_rect()

# Define a color
WHITE = (255, 255, 255)


# Create a Sprite class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Load an image or create a surface
        self.image = idle4

        # Set a rect for positioning
        self.rect = self.image.get_rect().inflate(1.2, 1)
        self.y_vel = 0
        self.x_vel = 0
        self.in_portal = False

    def update(self):
        print(self.x_vel)
        keys = pygame.key.get_pressed()
        if self.x_vel > 0:
            self.image = idle4
        elif self.x_vel < 0:
            self.image = idle4_

        
        self.y_vel += 3
        if abs(self.x_vel) > 1.5:
            self.x_vel += self.x_vel * -0.10
        elif abs(self.x_vel) < 0.51:
            self.x_vel = 0
        elif self.x_vel < 1.5 and self.x_vel > 0.51:
            self.x_vel -= 0.5
        elif self.x_vel > -1.5 and self.x_vel < 0.51:
            self.x_vel += 0.5

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x_vel-= 1.25
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x_vel += 1.25

        # Move the player rect
        self.rect.x += self.x_vel
        if pygame.sprite.spritecollide(self, blocks, False):
            # Undo movement if collision occurs
            self.rect.x -= self.x_vel
            self.x_vel = 0

        
        self.on_ground = False
        self.rect.y += self.y_vel
        if pygame.sprite.spritecollide(self, blocks, False):
            # Undo movement if collision occurs
            self.rect.y -= self.y_vel
            if self.y_vel > 0:
                self.on_ground = True
            self.y_vel = 0
        
        if pygame.sprite.spritecollide(self, trampolines, False):
            self.y_vel = -50

        if pygame.sprite.spritecollide(self, potions, False):
            reset_player()

        touching_portals = pygame.sprite.spritecollide(self, portals, False)
        if touching_portals:
            if not self.in_portal and len(portals) > 1:
                portal = touching_portals[0]
                dest = next(p for p in portals if portal != p)
                player.rect.x = dest.rect.x
                player.rect.y = dest.rect.y
            self.in_portal = True
        else:
            self.in_portal = False



        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.y_vel = -30

# Create a sprite group and add the player
all_sprites = pygame.sprite.Group()

next_id = 1
tiles = pygame.sprite.Group()
class Tile(pygame.sprite.Sprite):
    image = None
    groups = (all_sprites, tiles)
    def __init__(self, x, y):
        super().__init__()
        for set in self.groups:
            set.add(self)

        # Set a rect for positioning
        self.rect = self.image.get_rect()
        self.rect.inflate_ip(-10, -10)
        self.rect.center = (x, y)
        global next_id
        self.id_num = next_id
        next_id += 1
    
    def remove(self):
        for set in self.groups:
            set.remove(self)

blocks = set()
class Block(Tile):
    image = pygame.image.load("images/tile1.png").convert()
    groups = (all_sprites, blocks, tiles)
        

trampolines = set()
class Trampoline(Tile):
    image = pygame.image.load("images/trampoline.webp").convert()
    groups = (all_sprites, trampolines, tiles)

potions = set()
class Potion(Tile):
    image = pygame.image.load("images/potion.png").convert()
    groups = (all_sprites, potions, tiles)

portals = set()
class Portal(Tile):
    image = pygame.image.load("images/portal.png").convert()
    groups = (all_sprites, portals, tiles)



with open("map.json") as file:
    levels = json.load(file)
# moved to map.json
# player_start = [(320, 0), (250, 0), (600, 300)]
level = 0

block_types = [
    Block,
    Trampoline,
    Potion,
    Portal,
]


player = Player()
all_sprites.add(player)

def reset_player():
    player.y_vel = 0
    player.x_vel = 0
    player.rect.x, player.rect.y = level["spawn"]

level = None
level_num = 0
def change_level(level_num):
    global level
    # need a list because we will be deleting them while iterating
    # and otherwise the set will throw an error
    for tile in list(tiles):
        tile.remove()
    level = levels[level_num]
    reset_player()
    map = level["map"]
    for r, row in enumerate(map):
        for c, block in enumerate(row):
            if block != 0:
                block_types[block - 1](c * 32 + 16, r * 32 + 16)
change_level(level_num)

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
        level_num += 1
        change_level(level_num)

    # Draw everything
    if free_falling:
        gross_elevation += 10
        player.y_vel = 0
        player.rect.y = 320
        print(gross_elevation)
    else:
        gross_elevation = 1000 + 20 * level_num + player.rect.y / 32
    if level_num == len(levels) - 1:
        free_falling = True
    screen.fill(WHITE)  # Clear the screen
    screen.blit(bg1, (0, 0))
    screen.blit(bg2, (0, (1000 - gross_elevation) * 0.05))
    screen.blit(bg3, (0, (1000 - gross_elevation) * 0.1))

    # draw player in front
    tiles.draw(screen)
    screen.blit(player.image, player.rect)

    # Flip the display
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(30)

pygame.quit()
sys.exit()
