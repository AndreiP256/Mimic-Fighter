import pygame
from config.game_settings import *
from game.enemy import Enemy
from game.player import Player

pygame.init()
screen_width, screen_height = get_screen_size()
screen = pygame.display.set_mode((screen_width, screen_height))

# Calculate the global scale
global_scale = get_global_scale(screen_width, screen_height)

# Create a player instance
player = Player()

# Create an enemy instance with a spritesheet and global scale
enemy = Enemy(PINK_SLIME_SPRITESHEET, frame_width=32, frame_height=32, num_frames=4, x=100, y=100, speed=PINK_SLIME_SPEED, attack_type='melee', scale=global_scale, player=player)

# Add both player and enemy to the all_sprites group
all_sprites = pygame.sprite.Group(enemy, player)

clock = pygame.time.Clock()

isRunning = True

while isRunning:
    delta_time = clock.tick(60) / 1000.0  # Limit to 60 FPS and convert to seconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False

    all_sprites.update(delta_time)

    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()