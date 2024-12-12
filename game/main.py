import pygame

from config.game_settings import *
from game.groups.all_sprites_group import AllSprites
from game.player.Camera import Camera
from game.player.InputHandler import InputHandler
from game.player.player import Player
from game.enemies.enemy_builder import EnemyBuilder
import random
from game.player.Vortex_attack import AnimatedVortex
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

sound_manager = SoundManager()
load_sfx()
sound_manager.play_music()

def load_level(level_path):
    sound_manager.play_sound("lvl_end")
    global tile_map, player, enemyList, coliHandler, enemy_builder, inputHandler
    all_sprites.empty()
    tile_map = TileMap(level_path, sprite_group=all_sprites, screen=screen, collison_group=collison_group)
    tile_map.setup()
    player_spawn_x, player_spawn_y = tile_map.player_spawn
    player = Player(spritesheet=HERO_SPRITESHEET, frame_width=HERO_SPRITESHEET_WIDTH, collision_tiles=collison_group, frame_height=HERO_SPRITESHEET_HEIGHT
                    , x=player_spawn_x, y=player_spawn_y, speed=HERO_SPEED, scale=HERO_SCALE, frame_rate=HERO_FRAMERATE,
                    roll_frame_rate=HERO_ROLL_FRAMERATE, slash_damage=HERO_SLASH_DAMAGE, chop_damage=HERO_CHOP_DAMAGE)
    all_sprites.add(player)
    enemyList = []
    coliHandler = ColisionHandler(enemyList)
    inputHandler = InputHandler(coliHandler)  # Initialize inputHandler
    enemy_builder = EnemyBuilder(player, coliHandler, collison_group, all_sprites)

    for coords in tile_map.enemy_tiles:
        enemy_dict = ENEMIES_NAMES
        x, y = coords
        enemy = enemy_builder.create_enemy(random.choice(enemy_dict), x, y)
        enemyList.append(enemy)
        coliHandler.add_enemy(enemy)


def all_enemies_defeated():
    return all(enemy.health <= 0 for enemy in enemyList)

levels = [LEVEL_1_TMX_PATH, LEVEL_2_TMX_PATH, LEVEL_3_TMX_PATH, LEVEL_4_TMX_PATH, LEVEL_BOSS_TMX_PATH]
current_level = 0


isRunning = True
isPaused = False

pauseScreen = PauseScreen(screen, RESUME_BUTTON, RESTART_BUTTON, EXIT_BUTTON)
mainMenu = MainMenuScreen(screen, START_BUTTON, EXIT_BUTTON, bg_color="black", bg_image_path=MENU_BACKGROUND_IMAGE)
deathScreen = DeathScreen(screen, RESTART_BUTTON, EXIT_BUTTON, text_image_path=DEATH_TEXT_IMAGE, bg_image_path=DEATH_BACKGROUND_IMAGE)
if mainMenu.do_menu_loop() == "exit":
    isRunning = False

load_level(levels[current_level])
fade_in(screen, screen_width, screen_height, tile_map, all_sprites, enemyList, player)  # Call fade_in after loading the first level

while isRunning:
    if isPaused:
        pause_result = pauseScreen.do_pause_loop()
        if pause_result == "exit":
            isRunning = False
        elif pause_result == "restart":
            load_level(levels[current_level])
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
    anim = AnimatedVortex(0, 0, 1, './game/assets/images/vortex/frame', all_sprites)
    all_sprites.update(delta_time)
    if player.isDead:
        sound_manager.play_sound('player_die')
        res: str = deathScreen.do_death_loop()
        if res == "exit":
            isRunning = False
        elif res == "restart":
            tile_map.reset()
            load_level(levels[0])
            fade_in(screen, screen_width, screen_height, tile_map, all_sprites, enemyList, player)
        continue

    if all_enemies_defeated():
        tile_map.reset()
        fade_out(screen, screen_width, screen_height, tile_map, all_sprites, enemyList, player)
        current_level += 1
        if current_level < len(levels):
            load_level(levels[current_level])
            fade_in(screen, screen_width, screen_height, tile_map, all_sprites, enemyList, player)  # Call fade_in after loading the next level
        else:
            print("All levels completed!")
            isRunning = False

    screen.fill((0, 0, 0))
    all_sprites.draw(player.rect.center)
    # player.draw_debug(screen)
    # player.draw_adjusted_collision_rect(screen)
    player.healthBar.draw(screen)
    pygame.display.flip()

    # Check for health drop collection
    for health_drop in pygame.sprite.spritecollide(player, all_sprites, False):
        if isinstance(health_drop, HealthDrop) and health_drop.rect.colliderect(player.collision_rect):
            health_drop.apply_to(player)


pygame.quit()