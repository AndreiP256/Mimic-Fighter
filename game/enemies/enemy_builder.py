# enemy_builder.py
from game.enemies.slime_enemy import SlimeEnemy
from config.game_settings import *
from game.player.player import Player
class EnemyBuilder:
    def __init__(self, player:Player, colisionHandler, collision_tiles, sprites_group):
        self.player = player
        self.collision_tiles = collision_tiles
        self.colisionHandler = colisionHandler
        self.sprites_group = sprites_group
        self.enemy_types = {
            'pink_slime': (PINK_SLIME_SPRITESHEET, PINK_SLIME_SPEED, PINK_SLIME_SCALE, PINK_SLIME_HEALTH, PINK_SLIME_ATTACK_DAMAGE, PINK_SLIME_ATTACK_RANGE, SLIME_WANDER_TIME),
            'blue_slime': (BLUE_SLIME_SPRITESHEET, BLUE_SLIME_SPEED, BLUE_SLIME_SCALE, BLUE_SLIME_HEALTH, BLUE_SLIME_ATTACK_DAMAGE, BLUE_SLIME_ATTACK_RANGE, SLIME_WANDER_TIME),
            'green_slime': (GREEN_SLIME_SPRITESHEET, GREEN_SLIME_SPEED, GREEN_SLIME_SCALE, GREEN_SLIME_HEALTH, GREEN_SLIME_ATTACK_DAMAGE, GREEN_SLIME_ATTACK_RANGE, SLIME_WANDER_TIME)
        }

    def create_enemy(self, enemy_type, x, y):
        if enemy_type in self.enemy_types:
            spritesheet, speed, scale, health, attack_damage, attack_range, wander_time = self.enemy_types[enemy_type]
            return SlimeEnemy(sprites_group = self.sprites_group, spritesheet=spritesheet, wander_time=wander_time, colisionHandler=self.colisionHandler, frame_width=32, frame_height=32, attack_damage=attack_damage, attack_range=attack_range, num_frames=4, x=x, y=y, speed=speed, attack_type='mele', scale=scale, health=health, player = self.player, colision_tiles = self.collision_tiles)
        else:
            raise ValueError(f"Unknown enemy type: {enemy_type}")