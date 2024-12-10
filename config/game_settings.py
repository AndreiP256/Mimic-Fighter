import pygame

def get_screen_size():
    pygame.init()
    info = pygame.display.Info()
    screen_width = info.current_w
    screen_height = info.current_h
    return screen_width, screen_height
def get_global_scale():
    screen_width, screen_height = get_screen_size()
    scale_x = screen_width // num_tiles_x
    scale_y = screen_height // num_tiles_y
    return min(scale_x, scale_y) // tile_size

PINK_SLIME_SPRITESHEET = './assets/images/slimes/pink_slime/pink_slime_idle.png'
PINK_SLIME_SPEED = 125
PINK_SLIME_SCALE = 1
PINK_SLIME_HEALTH = 100
PINK_SLIME_ATTACK_DAMAGE = 10
PINK_SLIME_ATTACK_RANGE = 10

BLUE_SLIME_SPRITESHEET = './assets/images/slimes/blue_slime/blue_slime_idle.png'
BLUE_SLIME_SPEED = 100
BLUE_SLIME_SCALE = 2
BLUE_SLIME_HEALTH = 150
BLUE_SLIME_ATTACK_DAMAGE = 20
BLUE_SLIME_ATTACK_RANGE = 10
BLUE_SLIME_SCALE = 1.5

GREEN_SLIME_SPRITESHEET = './assets/images/slimes/green_slime/green_slime_idle.png'
GREEN_SLIME_SPEED = 145
GREEN_SLIME_SCALE = 1
GREEN_SLIME_HEALTH = 75
GREEN_SLIME_ATTACK_DAMAGE = 5
GREEN_SLIME_ATTACK_RANGE = 50



SLIME_WANDER_TIME = 5000
ENEMY_LOST_PLAYER_TIME = 3000
ENEMY_DETECTION_RADIUS = 200
ENEMY_ATTACK_COOLDOWN = 1000
ENEMY_SLOW_TIME = 500
ENEMY_SLOW_SPEED = 50

HERO_SPRITESHEET = './assets/images/hero/hero.png'
HERO_SPRITESHEET_WIDTH = 64
HERO_SPRITESHEET_HEIGHT = 65
HERO_SPEED = 200
HERO_SCALE = 3
HERO_FRAMERATE = 60
HERO_ROLL_FRAMERATE = 75
HERO_SPRINT_MULTIPLIER = 1.5
HERO_ROLL_MULTIPLIER = 5
HERO_SLASH_DAMAGE = 20
HERO_CHOP_DAMAGE = 40



num_tiles_x = 20
num_tiles_y = 15
tile_size = 32


SLASH_DIMENSIONS = (100, 100)
CHOP_DIMENSIONS = (25, 100)

HEALTHBAR_OFFSET_Y = -10
HEALTHBAR_OFFSET_X = -10
HEALTHBAR_WIDTH = 10
PLAYER_BAR_HEIGHT = 20
PLAYER_BAR_WIDTH = get_screen_size()[0] // 4
PLAYER_BAR_Y = 10
PLAYER_BAR_X = 10
DASH_COOLDOWN = 1000