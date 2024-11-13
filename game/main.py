from config.game_settings import *
from game.enemies.enemy import Enemy
from game.enemies.slime_enemy import SlimeEnemy
from game.player import Player
from game.enemies.enemy_builder import EnemyBuilder
import random

pygame.init()
screen_width, screen_height = get_screen_size()
screen = pygame.display.set_mode((screen_width, screen_height))

# Calculate the global scale

# Create a player instance
player = Player()

# Create an enemy builder instance
enemy_builder = EnemyBuilder(player)
enemyList = []

# Add both player and enemy to the all_sprites group
all_sprites = pygame.sprite.Group(player)

for i in range(100):
    dict = ['pink_slime', 'blue_slime', 'green_slime']
    enemy = enemy_builder.create_enemy(random.choice(dict), random.randint(0, screen_width), random.randint(0, screen_height))
    all_sprites.add(enemy)
    enemyList.append(enemy)

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