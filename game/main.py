from config.game_settings import *
from game.enemies.enemy import Enemy
from game.enemies.slime_enemy import SlimeEnemy
from game.player import Player

pygame.init()
screen_width, screen_height = get_screen_size()
screen = pygame.display.set_mode((screen_width, screen_height))

# Calculate the global scale

# Create a player instance
player = Player()

# Create an enemy instance with a spritesheet and global scale
pinkSlime = SlimeEnemy(PINK_SLIME_SPRITESHEET, 32, 32, 4, 100, 100, PINK_SLIME_SPEED, 'mele', PINK_SLIME_SCALE, player)
blueSlime = SlimeEnemy(BLUE_SLIME_SPRITESHEET, 32, 32, 4, 200, 200, BLUE_SLIME_SPEED, 'mele', BLUE_SLIME_SCALE, player)
greenSlime = SlimeEnemy(GREEN_SLIME_SPRITESHEET, 32, 32, 4, 300, 300, GREEN_SLIME_SPEED, 'mele', GREEN_SLIME_SCALE, player)

# Add both player and enemy to the all_sprites group
all_sprites = pygame.sprite.Group(pinkSlime, blueSlime, greenSlime, player)

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