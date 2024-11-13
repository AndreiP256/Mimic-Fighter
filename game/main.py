import pygame
from config.game_settings import get_screen_size

pygame.init()
screen = pygame.display.set_mode(get_screen_size())

isRunning = True

while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False

    pygame.display.update()

pygame.quit()
