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

SKELETON1_SPRITESHEET = './game/assets/images/skeletons/skeleton1.png'
SKELETON1_SPEED = 100
SKELETON1_SCALE = 1.5
SKELETON1_HEALTH = 100
SKELETON1_ATTACK_DAMAGE = 10
SKELETON1_ATTACK_RANGE = 10
SKELETON1_WANDER_TIME = 5000

SKELETON2_SPRITESHEET = './game/assets/images/skeletons/skeleton2.png'
SKELETON2_SPEED = 90
SKELETON2_SCALE = 1.6
SKELETON2_HEALTH = 150
SKELETON2_ATTACK_DAMAGE = 15
SKELETON2_ATTACK_RANGE = 8
SKELETON2_WANDER_TIME = 4500

SKULL_SPRITESHEET = './game/assets/images/skeletons/skull.png'
SKULL_SPEED = 160
SKULL_SCALE = 1.2
SKULL_HEALTH = 80
SKULL_ATTACK_DAMAGE = 8
SKULL_ATTACK_RANGE = 8
SKULL_WANDER_TIME = 6000

FLAME_SKULL_SPRITESHEET = './game/assets/images/fire_skull/fire_skull.png'
FLAME_PROJECTLE_PATH = './game/assets/images/fire_skull/fireball.png'
FLAME_SKULL_SPEED = 50
FLAME_SKULL_SCALE = 1.5
FLAME_SKULL_HEALTH = 50
FLAME_SKULL_ATTACK_DAMAGE = 5
FLAME_SKULL_ATTACK_RANGE = 500
FLAME_SKULL_WANDER_TIME = 5000

BLUE_SKULL_SPRITESHEET = './game/assets/images/blue_skull/blue_skull.png'
BLUE_PROJECTLE_PATH = './game/assets/images/blue_skull/blueball.png'
BLUE_SKULL_SPEED = 1
BLUE_SKULL_SCALE = 1.75
BLUE_SKULL_HEALTH = 100
BLUE_SKULL_ATTACK_DAMAGE = 15
BLUE_SKULL_ATTACK_RANGE = 400
BLUE_SKULL_WANDER_TIME = 5000

ENEMIES_NAMES = ['pink_slime', 'blue_slime', 'green_slime', 'skeleton1', 'skeleton2', 'skull_skeleton', 'flame_skull', 'blue_skull']



SLIME_WANDER_TIME = 5000
ENEMY_LOST_PLAYER_TIME = 3000
ENEMY_DETECTION_RADIUS = 700
ENEMY_ATTACK_COOLDOWN = 1000
ENEMY_SLOW_TIME = 500
ENEMY_SLOW_SPEED = 50
KNOCKBACK_DISTANCE = 10
KNOCKBACK_DURATION = 0.2 #in seconda

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
HERO_SLASH_DAMAGE = 10
HERO_CHOP_DAMAGE = 15
SLASH_DIMENSIONS = (100, 75)
CHOP_DIMENSIONS = (40, 100)
ATTACK_COOLDOWN = 250

screen_width, screen_height = get_screen_size()
num_tiles_x = 36
num_tiles_y = 22
tile_size = 16
TILE_SCALE = 3
DECOR_SCALE = 2
TILE_SIZE = 16

RESUME_BUTTON = './game/assets/images/buttons/Resume/Resume'
RESTART_BUTTON = './game/assets/images/buttons/Restart/Restart'
EXIT_BUTTON = './game/assets/images/buttons/Quit/Quit'
START_BUTTON = './game/assets/images/buttons/Start/Start'
SLASH_DIMENSIONS = (100, 100)
CHOP_DIMENSIONS = (25, 100)

LEVEL_1_TMX_PATH = "./game/assets/levels/level1/Tileset_lvl_1.tmx"
LEVEL_2_TMX_PATH = "./game/assets/levels/level2/Tileset_lvl_2.tmx"
LEVEL_3_TMX_PATH = "./game/assets/levels/level3/Tileset_lvl_3.tmx"
LEVEL_4_TMX_PATH = "./game/assets/levels/level4/Tileset_lvl_4.tmx"
LEVEL_5_TMX_PATH = "./game/assets/levels/level5/Tileset_lvl_5.tmx"
LEVEL_BOSS_TMX_PATH = "./game/assets/levels/boss/Tileset_boss.tmx"

HEALTHBAR_OFFSET_Y = -10
HEALTHBAR_OFFSET_X = -10
HEALTHBAR_WIDTH = 10
PLAYER_BAR_HEIGHT = 20
PLAYER_BAR_WIDTH = get_screen_size()[0] // 4
PLAYER_BAR_Y = 0
PLAYER_BAR_X = 0

ABILITY_BAR_X = SCREEN_WIDTH // 3 * 2
ABILITY_BAR_Y = 0
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

HEALTHDROP_IMAGE_PATH = './game/assets/images/healthdrop/flasks_1'
HEALTHDROP_CHANCE = 0.1
HEALTHDROP_AMOUNT = 10
HEALTHDROP_LIFETIME = 5000
HEALTHDROP_SCALE = 2.5
LOAD_TIME = 1000

HEALTHBAR_IMAGE_PATH = './game/assets/images/health/healthFill.png'
CONTOUR_IMAGE_PATH = './game/assets/images/health/healthContour.png'

ABILITY_IMAGE_PATH = './game/assets/images/health/abilityFill.png'
ABILITY_CONTOUR_IMAGE_PATH = './game/assets/images/health/abilityContour.png'

HEALTHBAR_SCALE_FACTOR = 5

VORTEX_PATH = './game/assets/images/vortex/frame'
VORTEX_SCALE = 3.5
SPECIAL_ENEMIES_KILLED = 10

MUSIC_PATH = './game/assets/sounds/music.wav'
SFX_DICT = {
    'slash': './game/assets/sounds/SFX/slash.wav',
    'chop': './game/assets/sounds/SFX/chop.wav',
    'roll': './game/assets/sounds/SFX/roll.wav',
    'sprint': './game/assets/sounds/SFX/sprint.wav',
    'enemy_attack': './game/assets/sounds/SFX/enemy_attack.wav',
    'enemy_hit': './game/assets/sounds/SFX/enemy_hit.wav',
    'lvl_end': './game/assets/sounds/SFX/lvl_end.wav',
    'human_damage': './game/assets/sounds/SFX/human_damage.wav',
    'healthdrop': './game/assets/sounds/SFX/health.wav',
    'player_die': './game/assets/sounds/SFX/player_die.wav',
    'vortex': './game/assets/sounds/SFX/vortex.wav',
}

VORTEX_DAMAGE = 50
VORTEX_RADIUS = 150

MOMO_MAMA_SPRITESHEET = './game/assets/images/momo_mama/momo_mama.png'
MOMO_MAMA_SPEED = 100
MOMO_MAMA_SCALE = 1.5
MOMO_MAMA_HEALTH = 200
MOMO_MAMA_ATTACK_DAMAGE = 20
MOMO_MAMA_ATTACK_RANGE = 50
MOMO_MAMA_WANDER_TIME = 5000
MOMO_PROJECTILE_PATH = './game/assets/images/blue_skull/blueball.png'

