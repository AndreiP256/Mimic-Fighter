import pygame

from config.game_settings import *
from game.player.InputHandler import InputHandler
from game.player.player import Player
from game.enemies.enemy_builder import EnemyBuilder
import random

from game.screens.menu_screen import MainMenuScreen
from game.screens.pause_screen import PauseScreen
from game.sprites.colision_handler import *


pygame.init()
screen_width, screen_height = get_screen_size()
screen = pygame.display.set_mode((screen_width - 100, screen_height - 100))


# Create a player instance
player = Player(spritesheet=HERO_SPRITESHEET, frame_width=HERO_SPRITESHEET_WIDTH, frame_height=HERO_SPRITESHEET_HEIGHT
                , x=screen_width // 2, y=screen_height // 2, speed=HERO_SPEED, scale=HERO_SCALE, frame_rate=HERO_FRAMERATE,
                roll_frame_rate=HERO_ROLL_FRAMERATE, slash_damage=HERO_SLASH_DAMAGE, chop_damage=HERO_CHOP_DAMAGE)
all_sprites = pygame.sprite.Group(player)

# Create an enemy builder instance
enemyList = []

# Initliaze input handler
coliHandler = ColisionHandler(enemyList)
inputHandler = InputHandler(coliHandler=coliHandler)
enemy_builder = EnemyBuilder(player, coliHandler)

# Initialize global clock
clock = pygame.time.Clock()


# Create 100 enemies
for i in range(10):
    dict = ['pink_slime', 'blue_slime', 'green_slime']
    enemy = enemy_builder.create_enemy(random.choice(dict), random.randint(0, screen_width), random.randint(0, screen_height))
    all_sprites.add(enemy)
    enemyList.append(enemy)
    coliHandler.add_enemy(enemy)


isRunning = True
isPaused = False

pauseScreen = PauseScreen(screen, RESUME_BUTTON, RESTART_BUTTON, EXIT_BUTTON)
mainMenu = MainMenuScreen(screen, START_BUTTON, EXIT_BUTTON, bg_color="black")

if mainMenu.do_menu_loop() == "exit":
    isRunning = False

while isRunning:
    if isPaused:
        if pauseScreen.do_pause_loop() == "exit":
            isRunning = False
        isPaused = False
        continue
    delta_time = clock.tick(60) / 1000.0  # Limit to 60 FPS and convert to seconds
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
            pygame.quit()
            break
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            isPaused = not isPaused
            continue
        inputHandler(event, player, isPaused)
    keys = pygame.key.get_pressed()
    inputHandler.handle_key(player, keys)
    all_sprites.update(delta_time)
    screen.fill((0, 0, 0))
    coliHandler.draw_rectangle(screen, player, SLASH_DIMENSIONS[0], SLASH_DIMENSIONS[1], (255, 0, 0))
    coliHandler.draw_rectangle(screen, player, CHOP_DIMENSIONS[0], CHOP_DIMENSIONS[1], (0, 255, 0))
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()