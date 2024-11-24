import pygame, pygame.draw
import json
from math import copysign
from random import randint

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
gross_elevation = 1000
free_falling = False
pygame.mixer.music.load("audio/background.ogg")
jump_sound = pygame.mixer.Sound("audio/jump.ogg")
woosh_sound = pygame.mixer.Sound("audio/woosh.ogg")
pygame.mixer.music.play(loops=-1)
# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Why won't you let me leave")
idle4 = pygame.image.load("images/player/idle/sprite_0.png").convert_alpha()
idle4_ = pygame.image.load("images/player/idle/sprite_1.png").convert_alpha()
bg1 = pygame.transform.scale_by(pygame.image.load("images/background/01background.png"), 2).convert_alpha()
bg2 = pygame.transform.scale_by(pygame.image.load("images/background/02background.png"), 2).convert_alpha()
bg3 = pygame.transform.scale_by(pygame.image.load("images/background/03background.png"), 2).convert_alpha()
credits_image = pygame.image.load("images/text/credits.png").convert_alpha()
cred_rect = credits_image.get_rect()
title_image = pygame.transform.scale_by(pygame.image.load("images/title.png"), 7).convert_alpha()
cred_rect.center = (400, 1000)
rect1 = idle4.get_rect()
rect2 = idle4_.get_rect()
title_screen = True
title_rect = title_image.get_rect()
title_rect.center = (400, 280)
# Define a color
WHITE = (255, 255, 255)


# Create a Sprite class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Load an image or create a surface
        self.image = idle4

        # Set a rect for positioning
        # why is it inflated?
        self.rect = self.image.get_rect()#.inflate(1.2, 1)
        self.y_vel = 0
        self.x_vel = 0
        self.in_portal = False

    def move_y(self, pixels):
        if pixels == 0:
            return True
        # prevent phasing through walls
        if abs(pixels) > 30:
            for _ in range(pixels // 30):
                if not self.move_y(copysign(30, pixels)):
                    return False
            return self.move_y(copysign(abs(pixels % 30), pixels))
        # moving down
        if pixels > 0:
            old_y = self.rect.bottom
        else:
            old_y = self.rect.top
        self.rect.y += pixels
        collided_blocks = pygame.sprite.spritecollide(self, blocks, False)
        if not collided_blocks:
            return True

        # Undo movement if collision occurs

        if pixels > 0:
            min_y = min(block.rect.top for block in collided_blocks)
            self.rect.bottom = max(min_y, old_y)
            # print(f"down {min_y=}, {old_y=}")
        else:
            max_y = max(block.rect.bottom for block in collided_blocks)
            # print(f"up {max_y=}, {old_y=}")
            self.rect.top = min(max_y, old_y)

        return False

    def move_x(self, pixels):
        if pixels == 0:
            return True
        # prevent phasing through walls
        if abs(pixels) > 30:
            for _ in range(pixels // 30):
                if not self.move_x(copysign(30, pixels)):
                    return False
            return self.move_x(copysign(abs(pixels % 30), pixels))
        # moving down
        if pixels > 0:
            old_x = self.rect.right
        else:
            old_x = self.rect.left
        self.rect.x += pixels
        collided_blocks = pygame.sprite.spritecollide(self, blocks, False)
        if not collided_blocks:
            return True

        # Undo movement if collision occurs

        if pixels > 0:
            min_x = min(block.rect.left for block in collided_blocks)
            self.rect.right = max(min_x, old_x)
            # print(f"down {min_y=}, {old_y=}")
        else:
            max_x = max(block.rect.right for block in collided_blocks)
            # print(f"up {max_y=}, {old_y=}")
            self.rect.left = min(max_x, old_x)

        return False

    def update(self):
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
        if not self.move_x(self.x_vel):
            self.x_vel = 0

        # returns false on collision
        self.on_ground = False
        if not self.move_y(self.y_vel):
            if self.y_vel > 0:
                self.on_ground = True
            self.y_vel = 0
        
        if pygame.sprite.spritecollide(self, trampolines, False):
            self.y_vel = -70
            jump_sound.play()

        if pygame.sprite.spritecollide(self, potions, False):
            reset_player()

        touching_portals = pygame.sprite.spritecollide(self, portals, False)
        if touching_portals:
            if not self.in_portal and len(portals) > 1:
                portal = touching_portals[0]
                dest = next(p for p in portals if portal != p)
                player.rect.x = dest.rect.x
                player.rect.y = dest.rect.y
                woosh_sound.play()
                # print(f"{pygame.sprite.spritecollide(self, blocks, False)=}")
                # print(f"{player.rect=}")
                # print(f"{dest.rect=}")
            self.in_portal = True
        else:
            self.in_portal = False



        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.y_vel = -30
            jump_sound.play()

# Create a sprite group and add the player
all_sprites = pygame.sprite.Group()

next_id = 1
tiles = pygame.sprite.Group()
class Tile(pygame.sprite.Sprite):
    image = None
    groups = (all_sprites, tiles)
    collison = None
    def __init__(self, x, y):
        super().__init__()
        for set in self.groups:
            set.add(self)

        # Set a rect for positioning
        self.rect = self.image.get_rect()
        # self.rect.inflate_ip(-10, -10)
        self.rect.center = (x, y)
        global next_id
        self.id_num = next_id
        next_id += 1
    
    def remove(self):
        for set in self.groups:
            set.remove(self)

level = None
level_num = 0


blocks = set()
class Block(Tile):
    image = pygame.image.load("images/tile1.png").convert()
    groups = (all_sprites, blocks, tiles)
        

trampolines = set()
class Trampoline(Tile):
    image = pygame.image.load("images/trampoline.webp").convert_alpha()
    groups = (all_sprites, trampolines, tiles)

potions = set()
class Potion(Tile):
    image = pygame.image.load("images/potion.png").convert_alpha()
    groups = (all_sprites, potions, tiles)

portals = set()
class Portal(Tile):
    image = pygame.image.load("images/portal.png").convert_alpha()
    groups = (all_sprites, portals, tiles)

texts = set()
class Text(pygame.sprite.Sprite):
    groups = (all_sprites, texts, tiles)

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(f"images/text/text_{level_num + 1}.png").convert_alpha()
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

class Cloud(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale_by(pygame.image.load(f"images/clouds/cloud{randint(1, 2)}.png"), randint(1, 50)/100).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = x, y

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
    Text,
]


player = Player()
all_sprites.add(player)

def reset_player():
    player.y_vel = 0
    player.x_vel = 0
    player.rect.x, player.rect.y = level["spawn"]

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
current_clouds = []
# Main game loop
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()
    # Update sprites
    all_sprites.update()

    if player.rect.y > 900:
        level_num += 1
        change_level(level_num)
    elif player.rect.y < -100 and level_num > 0:
        level_num -= 1
        change_level(level_num)

    # Draw everything
    if free_falling:
        gross_elevation += 1
        cred_rect.y -= 2
        player.y_vel = 0
        player.rect.y -= 2.5
        print(gross_elevation)
        if len(current_clouds) < 1:
            for i in range(5):
                current_clouds.append(Cloud(randint(100, 560), randint(900, 3000)))
        for i in range(len(current_clouds)):
            if current_clouds[i].rect.y < -500:
                current_clouds[i].rect.y = randint(800, 1000)
                current_clouds[i].rect.x = randint(100, 560)
            current_clouds[i].rect.y -= 4

    else:
        gross_elevation = 1000 + 20 * level_num + player.rect.y / 32
    if level_num == len(levels) - 1:
        free_falling = True
    # -----SCREEN DRAWING-----
    screen.fill(WHITE)  # Clear the screen
    screen.blit(bg1, (0, 0))
    screen.blit(bg2, (0, (1000 - gross_elevation) * 0.05))
    screen.blit(bg3, (0, (1000 - gross_elevation) * 0.1))
    if not title_screen:
        for i in range(len(current_clouds)):
            screen.blit(current_clouds[i].image, current_clouds[i].rect)
            print(f"rendering cloud at {current_clouds[i].rect.x}, {current_clouds[i].rect.y}")
        # draw player in front
        if free_falling:
            screen.blit(credits_image, cred_rect)
        tiles.draw(screen)
        screen.blit(player.image, player.rect)
    if title_screen:
        screen.blit(title_image, title_rect)
        if (keys[pygame.K_RETURN] or keys[pygame.K_SPACE] or mouse[0]):
            title_screen = False
    # pygame.draw.rect(screen, "red", player.rect, 2)
    # for obj in trampolines:
    #     pygame.draw.rect(screen, "blue", obj.rect, 2)

    # Flip the display
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(30)

pygame.quit()