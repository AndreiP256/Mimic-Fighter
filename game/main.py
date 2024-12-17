import pygame

from config.game_settings import *
from game.groups.all_sprites_group import AllSprites
from game.player.input_handler import InputHandler
from game.player.player import Player
from game.enemies.enemy_builder import EnemyBuilder
import random
from game.screens.fades import fade_out, fade_in
from game.screens.death_screen import DeathScreen
from game.screens.menu_screen import MainMenuScreen
from game.screens.pause_screen import PauseScreen
from game.sprites.colision_handler import *
from game.sprites.tiles import TileMap
from game.enemies.healthdrop import HealthDrop
from game.sounds.sfx_loader import load_sfx
from game.sounds.sound_manager import SoundManager

pygame.init()
screen_width, screen_height = get_screen_size()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()  # Initialize the clock
all_sprites = AllSprites()
collison_group = pygame.sprite.Group()
all_enemies = pygame.sprite.Group()
coliHandler = ColisionHandler(all_enemies)
inputHandler = InputHandler(coliHandler)
enemy_builder = EnemyBuilder(None, coliHandler, collison_group, all_sprites, all_enemies)
momo_mama = None
player = Player(0, 0, collison_group, all_sprites)
sound_manager = SoundManager()
load_sfx()
sound_manager.play_music()


def load_level(level_path):
    sound_manager.play_sound("lvl_end")
    global tile_map, coliHandler, inputHandler, momo_mama
    all_sprites.empty()
    tile_map = TileMap(level_path, sprite_group=all_sprites, screen=screen, collison_group=collison_group)
    tile_map.setup()
    player_spawn_x, player_spawn_y = tile_map.player_spawn
    player.reset_player(player_spawn_x, player_spawn_y, all_sprites)
    enemy_builder.set_player(player)
    for coords in tile_map.enemy_tiles:
        enemy_dict = ENEMIES_NAMES
        x, y = coords
        enemy_builder.create_enemy(random.choice(enemy_dict), x, y)
    if tile_map.boss_tile:
        x, y = tile_map.boss_tile
        momo_mama = enemy_builder.create_enemy('momo_mama', x, y, enemy_builder)


def all_enemies_defeated():
    return all_enemies.__len__() == 0

levels = [LEVEL_1_TMX_PATH, LEVEL_2_TMX_PATH, LEVEL_3_TMX_PATH, LEVEL_4_TMX_PATH, LEVEL_5_TMX_PATH, LEVEL_6_TMX_PATH,  LEVEL_BOSS_TMX_PATH]
current_level = STARTING_LEVEL


isRunning = True
isPaused = False

pauseScreen = PauseScreen(screen, RESUME_BUTTON, RESTART_BUTTON, EXIT_BUTTON)
mainMenu = MainMenuScreen(screen, START_BUTTON, EXIT_BUTTON, bg_color="black", bg_image_path=MENU_BACKGROUND_IMAGE)
deathScreen = DeathScreen(screen, RESTART_BUTTON, EXIT_BUTTON, text_image_path=DEATH_TEXT_IMAGE, bg_image_path=DEATH_BACKGROUND_IMAGE)
if mainMenu.do_menu_loop() == "exit":
    isRunning = False
    pygame.quit()

load_level(levels[current_level])
fade_in(screen, screen_width, screen_height, all_sprites, player)  # Call fade_in after loading the first level
start_time = pygame.time.get_ticks()  # Record the start time
while isRunning:
    if isPaused:
        pause_result = pauseScreen.do_pause_loop()
        if pause_result == "exit":
            isRunning = False
        elif pause_result == "restart":
            load_level(levels[current_level])
            fade_in(screen, screen_width, screen_height, all_sprites, player)
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

    if pygame.time.get_ticks() - start_time > LOAD_TIME:  # Check if more than one second has passeddd
        inputHandler.handle_key(player, keys)  # Use inputHandler
    all_sprites.update(delta_time)

    if player.isDead:
        sound_manager.play_sound('player_die')
        res: str = deathScreen.do_death_loop()
        if res == "exit":
            isRunning = False
        elif res == "restart":
            tile_map.reset()
            load_level(levels[STARTING_LEVEL])
            fade_in(screen, screen_width, screen_height, all_sprites, player)
        continue

    if all_enemies_defeated():
        tile_map.reset()
        fade_out(screen, screen_width, screen_height, all_sprites, player)
        current_level += 1
        if current_level < len(levels):
            load_level(levels[current_level])
            fade_in(screen, screen_width, screen_height, all_sprites, player) # Call fade_in after loading the next level
        else:
            endScreen = MainMenuScreen(screen, START_BUTTON, EXIT_BUTTON, bg_color="black", bg_image_path=VICTORY_SCREEN)
            if endScreen.do_menu_loop() == "exit":
                isRunning = False
            elif endScreen.do_menu_loop() == "start":
                load_level(levels[STARTING_LEVEL])
                current_level = STARTING_LEVEL
                fade_in(screen, screen_width, screen_height, all_sprites, player)

    screen.fill((0, 0, 0))
    all_sprites.draw(player.rect.center)
    player.healthBar.draw(screen)
    if(momo_mama):
        momo_mama.health_bar.draw(screen)
    player.abilityBar.draw(screen)
    player.draw_kills(screen)
    #coliHandler.draw_rectangle(screen, player, *CHOP_DIMENSIONS, pygame.Color('red'))
    pygame.display.flip()

    # Check for health drop collection
    for health_drop in pygame.sprite.spritecollide(player, all_sprites, False):
        if isinstance(health_drop, HealthDrop) and health_drop.rect.colliderect(player.collision_rect):
            health_drop.apply_to(player)


pygame.quit()