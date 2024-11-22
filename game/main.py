import pygame

from config.game_settings import *
from game.player.InputHandler import InputHandler
from game.player.player import Player
from game.enemies.enemy_builder import EnemyBuilder
import random

from game.sprites.colision_handler import *

pygame.init()
screen_width, screen_height = get_screen_size()
screen = pygame.display.set_mode((screen_width - 100, screen_height - 100))


# Create a player instance
player = Player(spritesheet=HERO_SPRITESHEET, frame_width=HERO_SPRITESHEET_WIDTH, frame_height=HERO_SPRITESHEET_HEIGHT
                , x=screen_width // 2, y=screen_height // 2, speed=HERO_SPEED, scale=HERO_SCALE, frame_rate=HERO_FRAMERATE,
                roll_frame_rate=HERO_ROLL_FRAMERATE)
all_sprites = pygame.sprite.Group(player)

# Create an enemy builder instance
enemyList = []

# Initliaze input handler
inputHandler = InputHandler()
coliHandler = ColisionHandler(enemyList)
enemy_builder = EnemyBuilder(player, coliHandler)

# Initialize global clock
clock = pygame.time.Clock()

# Initliaze input handler

inputHandler = InputHandler()

# Create 100 enemies
for i in range(10):
    dict = ['pink_slime', 'blue_slime', 'green_slime']
    enemy = enemy_builder.create_enemy(random.choice(dict), random.randint(0, screen_width), random.randint(0, screen_height))
    all_sprites.add(enemy)
    enemyList.append(enemy)
    coliHandler.add_enemy(enemy)


isRunning = True

while isRunning:
    delta_time = clock.tick(60) / 1000.0  # Limit to 60 FPS and convert to seconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
            pygame.quit()
            break
        inputHandler(event, player)

    keys = pygame.key.get_pressed()
    inputHandler.handle_key(player, keys)
    all_sprites.update(delta_time)

    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()