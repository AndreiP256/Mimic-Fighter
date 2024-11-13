import pygame
def get_screen_size():
    pygame.init()
    info = pygame.display.Info()
    screen_width = info.current_w
    screen_height = info.current_h
    return screen_width, screen_height