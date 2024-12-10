import pygame

from config.game_settings import *
from game.player.Camera import Camera
from game.player.InputHandler import InputHandler
from game.player.player import Player
from game.enemies.enemy_builder import EnemyBuilder
import random

from game.sprites.colision_handler import *
from game.sprites.tiles import TileMap

pygame.init()
screen_width, screen_height = get_screen_size()
screen = pygame.display.set_mode((screen_width, screen_height))




tile_map = TileMap(LEVEL_1_TMX_PATH, TILE_SCALE)
player = Player(spritesheet=HERO_SPRITESHEET, frame_width=HERO_SPRITESHEET_WIDTH, collision_tiles=tile_map.collision_tiles, frame_height=HERO_SPRITESHEET_HEIGHT
                , x=screen_width // 2 + 100, y=screen_height // 2, speed=HERO_SPEED, scale=HERO_SCALE, frame_rate=HERO_FRAMERATE,
                roll_frame_rate=HERO_ROLL_FRAMERATE, slash_damage=HERO_SLASH_DAMAGE, chop_damage=HERO_CHOP_DAMAGE)


all_sprites = pygame.sprite.Group(player)

# Create an enemy builder instance
enemyList = []

# Initliaze input handler
coliHandler = ColisionHandler(enemyList)
inputHandler = InputHandler(coliHandler=coliHandler)
enemy_builder = EnemyBuilder(player, coliHandler, tile_map.collision_tiles)

# Initialize global clock
clock = pygame.time.Clock()

# Initliaze input handler

inputHandler = InputHandler(coliHandler)

# Create 100 enemies
for i in range(1):
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
    tile_map.render(screen)
    # tile_map.render_collision_debug(screen, camera)
    # tile_map.render_collision_debug_no_camera(screen)
    # coliHandler.draw_rectangle(screen, player, SLASH_DIMENSIONS[0], SLASH_DIMENSIONS[1], (255, 0, 0))
    # coliHandler.draw_rectangle(screen, player, CHOP_DIMENSIONS[0], CHOP_DIMENSIONS[1], (0, 255, 0))
    all_sprites.draw(screen)
    # player.draw_debug(screen)
    # player.draw_adjusted_collision_rect(screen)
    pygame.display.flip()

pygame.quit()