import pygame

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900


def get_screen_size():
    pygame.init()
    info = pygame.display.Info()
    screen_width = SCREEN_WIDTH
    screen_height = SCREEN_HEIGHT
    return screen_width, screen_height
def get_global_scale():
    screen_width, screen_height = get_screen_size()
    scale_x = screen_width // num_tiles_x
    scale_y = screen_height // num_tiles_y
    return min(scale_x, scale_y) // tile_size

PINK_SLIME_SPRITESHEET = './game/assets/images/slimes/pink_slime/pink_slime_idle.png'
PINK_SLIME_SPEED = 125
PINK_SLIME_SCALE = 1
PINK_SLIME_HEALTH = 100
PINK_SLIME_ATTACK_DAMAGE = 10
PINK_SLIME_ATTACK_RANGE = 10

BLUE_SLIME_SPRITESHEET = './game/assets/images/slimes/blue_slime/blue_slime_idle.png'
BLUE_SLIME_SPEED = 100
BLUE_SLIME_SCALE = 2
BLUE_SLIME_HEALTH = 150
BLUE_SLIME_ATTACK_DAMAGE = 20
BLUE_SLIME_ATTACK_RANGE = 10
BLUE_SLIME_SCALE = 1.5

GREEN_SLIME_SPRITESHEET = './game/assets/images/slimes/green_slime/green_slime_idle.png'
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

HERO_SPRITESHEET = './game/assets/images/hero/hero.png'
HERO_SPRITESHEET_WIDTH = 64
HERO_SPRITESHEET_HEIGHT = 65
HERO_SPEED = 200
HERO_SCALE = 3
HERO_FRAMERATE = 60
HERO_ROLL_FRAMERATE = 75
HERO_SPRINT_MULTIPLIER = 1.5
HERO_ROLL_MULTIPLIER = 2.5
ROLL_COOLDOWN = 750
HERO_SLASH_DAMAGE = 20
HERO_CHOP_DAMAGE = 30
SLASH_DIMENSIONS = (100, 75)
CHOP_DIMENSIONS = (40, 100)

screen_width, screen_height = get_screen_size()
num_tiles_x = 36
num_tiles_y = 22
tile_size = 16
TILE_SCALE = 3

RESUME_BUTTON = './game/assets/images/buttons/Resume/Resume1.png'
RESTART_BUTTON = './game/assets/images/buttons/Restart/Restart1.png'
EXIT_BUTTON = './game/assets/images/buttons/Quit/Quit1.png'
START_BUTTON = './game/assets/images/buttons/Start/Start1.png'
SLASH_DIMENSIONS = (100, 100)
CHOP_DIMENSIONS = (25, 100)

LEVEL_1_TMX_PATH = "./game/assets/levels/level1/Tileset_lvl_1.tmx"
LEVEL_2_TMX_PATH = "./game/assets/levels/level2/Tileset_lvl_2.tmx"
LEVEL_3_TMX_PATH = "./game/assets/levels/level3/Tileset_lvl_3.tmx"
LEVEL_4_TMX_PATH = "./game/assets/levels/level4/Tileset_lvl_4.tmx"
LEVEL_BOSS_TMX_PATH = "./game/assets/levels/boss/Tileset_boss.tmx"

LEVEL_1_SPAWN_X = 60
LEVEL_1_SPAWN_Y = 700

LEVEL_2_SPAWN_X = 1000
LEVEL_2_SPAWN_Y = 500

LEVEL_3_SPAWN_X = 60
LEVEL_3_SPAWN_Y = 800

LEVEL_4_SPAWN_X = 1500
LEVEL_4_SPAWN_Y = 800

LEVEL_BOSS_SPAWN_X = 100
LEVEL_BOSS_SPAWN_Y = 500

HEALTHBAR_OFFSET_Y = -10
HEALTHBAR_OFFSET_X = -10
HEALTHBAR_WIDTH = 10
PLAYER_BAR_HEIGHT = 20
PLAYER_BAR_WIDTH = get_screen_size()[0] // 4
PLAYER_BAR_Y = 20
PLAYER_BAR_X = 20
DASH_COOLDOWN = 1000

MENU_BACKGROUND_IMAGE = './game/assets/images/main_bg.png'
DEATH_TEXT_IMAGE = './game/assets/images/death_text.png'
DEATH_BACKGROUND_IMAGE = './game/assets/images/death_screen.png'
DEATH_IMAGE_WIDTH = 4120
DEATH_IMAGE_HEIGHT = 1000
IMAGE_SCALE = 0.2
BUTTON_SCALE = 8
BG_IMAGE_PATH = './game/assets/images/main_bg.png'
BUTTON_SCALE = 8

MARGIN = 20
NUM_ENEMIES = 15

HEALTHDROP_IMAGE_PATH = './game/assets/images/healthdrop.png'
HEALTHDROP_CHANCE = 0.1
HEALTHDROP_AMOUNT = 10
HEALTHDROP_LIFETIME = 5000
