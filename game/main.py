import pygame

from config.game_settings import *
from game.player.Camera import Camera
from game.player.InputHandler import InputHandler
from game.player.player import Player
from game.enemies.enemy_builder import EnemyBuilder
import random
from game.screens.fades import fade_out, fade_in

from game.screens.death_screen import DeathScreen
from game.screens.menu_screen import MainMenuScreen
from game.screens.pause_screen import PauseScreen
from game.sprites.colision_handler import *
from game.sprites.tiles import TileMap

pygame.init()
screen_width, screen_height = get_screen_size()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()  # Initialize the clock

def load_level(level_path, player_spawn_x, player_spawn_y):
    global tile_map, player, all_sprites, enemyList, coliHandler, enemy_builder, inputHandler
    tile_map = TileMap(level_path, TILE_SCALE)
    player = Player(spritesheet=HERO_SPRITESHEET, frame_width=HERO_SPRITESHEET_WIDTH, collision_tiles=tile_map.collision_tiles, frame_height=HERO_SPRITESHEET_HEIGHT
                    , x=player_spawn_x, y=player_spawn_y, speed=HERO_SPEED, scale=HERO_SCALE, frame_rate=HERO_FRAMERATE,
                    roll_frame_rate=HERO_ROLL_FRAMERATE, slash_damage=HERO_SLASH_DAMAGE, chop_damage=HERO_CHOP_DAMAGE)

    all_sprites = pygame.sprite.Group(player)
    enemyList = []
    coliHandler = ColisionHandler(enemyList)
    inputHandler = InputHandler(coliHandler)  # Initialize inputHandler
    enemy_builder = EnemyBuilder(player, coliHandler, tile_map.collision_tiles)

    for _ in range(NUM_ENEMIES):
        dict = ['pink_slime', 'blue_slime', 'green_slime']
        while True:
            x = random.randint(0, tile_map.width - 32)
            y = random.randint(0, tile_map.height - 32)
            enemy_rect = pygame.Rect(x, y, 32, 32)
            if not any(enemy_rect.colliderect(tile.inflate(MARGIN, MARGIN)) for tile in tile_map.collision_tiles):
                break
        enemy = enemy_builder.create_enemy(random.choice(dict), x, y)
        all_sprites.add(enemy)
        all_sprites.add(enemy.health_bar)
        enemyList.append(enemy)
        coliHandler.add_enemy(enemy)

def all_enemies_defeated():
    return all(enemy.health <= 0 for enemy in enemyList)

levels = [
    (LEVEL_1_TMX_PATH, LEVEL_1_SPAWN_X, LEVEL_1_SPAWN_Y),
    (LEVEL_2_TMX_PATH, LEVEL_2_SPAWN_X, LEVEL_2_SPAWN_Y),
    (LEVEL_3_TMX_PATH, LEVEL_3_SPAWN_X, LEVEL_3_SPAWN_Y),
    (LEVEL_4_TMX_PATH, LEVEL_4_SPAWN_X, LEVEL_4_SPAWN_Y),
    (LEVEL_BOSS_TMX_PATH, LEVEL_BOSS_SPAWN_X, LEVEL_BOSS_SPAWN_Y)
]

current_level = 0


isRunning = True
isPaused = False

pauseScreen = PauseScreen(screen, RESUME_BUTTON, RESTART_BUTTON, EXIT_BUTTON)
mainMenu = MainMenuScreen(screen, START_BUTTON, EXIT_BUTTON, bg_color="black", bg_image_path=MENU_BACKGROUND_IMAGE)
deathScreen = DeathScreen(screen, RESTART_BUTTON, EXIT_BUTTON, text_image_path=DEATH_TEXT_IMAGE, bg_image_path=DEATH_BACKGROUND_IMAGE)

if mainMenu.do_menu_loop() == "exit":
    isRunning = False

load_level(*levels[current_level])
fade_in(screen, screen_width, screen_height, tile_map, all_sprites, enemyList, player)  # Call fade_in after loading the first level

while isRunning:
    if isPaused:
        pause_result = pauseScreen.do_pause_loop()
        if pause_result == "exit":
            isRunning = False
        elif pause_result == "restart":
            load_level(*levels[current_level])
            fade_in(screen, screen_width, screen_height, tile_map, all_sprites, enemyList, player)
        isPaused = False
        player.stop()
        continue
    delta_time = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
            pygame.quit()
            break
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            isPaused = not isPaused
            continue
        inputHandler.handle_event(event, player)  # Use inputHandler
    keys = pygame.key.get_pressed()
    inputHandler.handle_key(player, keys)  # Use inputHandler
    all_sprites.update(delta_time)
    if player.isDead:
        res: str = deathScreen.do_death_loop()
        if res == "exit":
            isRunning = False
        elif res == "restart":
            load_level(*levels[0])
            fade_in(screen, screen_width, screen_height, tile_map, all_sprites, enemyList, player)
        continue

    if all_enemies_defeated():
        fade_out(screen, screen_width, screen_height, tile_map, all_sprites, enemyList, player)
        current_level += 1
        if current_level < len(levels):
            load_level(*levels[current_level])
            fade_in(screen, screen_width, screen_height, tile_map, all_sprites, enemyList, player)  # Call fade_in after loading the next level
        else:
            print("All levels completed!")
            isRunning = False

    screen.fill((0, 0, 0))
    tile_map.render(screen)
    all_sprites.draw(screen)
    # player.draw_debug(screen)
    # player.draw_adjusted_collision_rect(screen)
    player.healthBar.draw(screen)
    pygame.display.flip()

pygame.quit()