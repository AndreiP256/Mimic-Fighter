import pygame
from config.game_settings import *
from game.enemy import Enemy

pygame.init()
screen_width, screen_height = get_screen_size()
screen = pygame.display.set_mode((screen_width, screen_height))

# Define the number of tiles you want on the screen

# Calculate the global scale
global_scale = get_global_scale(screen_width, screen_height)

# Create an enemy instance with a spritesheet and global scale
enemy = Enemy(PINK_SLIME_SPRITESHEET, frame_width=32, frame_height=32, num_frames=4, x=100, y=100, speed=2, attack_type='melee', scale=global_scale)

all_sprites = pygame.sprite.Group(enemy)

isRunning = True

while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False

    all_sprites.update()

    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()