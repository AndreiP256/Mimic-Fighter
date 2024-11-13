import pygame

def get_screen_size():
    pygame.init()
    info = pygame.display.Info()
    screen_width = info.current_w
    screen_height = info.current_h
    return screen_width, screen_height

def get_global_scale(screen_width, screen_height):
    scale_x = screen_width // num_tiles_x
    scale_y = screen_height // num_tiles_y
    return min(scale_x, scale_y) // tile_size   # Adjust the scale to be relative to the tile size

PINK_SLIME_SPRITESHEET = './assets/images/slimes/pink_slime/pink_slime_idle.png'
num_tiles_x = 20
num_tiles_y = 15
tile_size = 32
