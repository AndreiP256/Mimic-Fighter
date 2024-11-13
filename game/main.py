from config.game_settings import *
from game.player.player import Player
from game.enemies.enemy_builder import EnemyBuilder
import random
from game.player.Input_handler import InputHandler
from game.sprites.colision_handler import *

pygame.init()
screen_width, screen_height = get_screen_size()
screen = pygame.display.set_mode((screen_width, screen_height))


# Create a player instance
player = Player()
all_sprites = pygame.sprite.Group(player)

# Create an enemy builder instance
enemyList = []

# Initliaze input handler
inputHandler = InputHandler()
coliHandler = ColisionHandler(enemyList)
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

while isRunning:
    delta_time = clock.tick(60) / 1000.0  # Limit to 60 FPS and convert to seconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        if(event.type == pygame.KEYDOWN or event.type == pygame.KEYUP or event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP):
            inputHandler(event, player)

    all_sprites.update(delta_time)

    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()