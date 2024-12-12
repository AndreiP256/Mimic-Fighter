# enemy_builder.py
from arrow.api import factory

from game.enemies.enemy_factory import EnemyFactory
from game.enemies.slime_enemy import SlimeEnemy
from config.game_settings import *
from game.player.player import Player
class EnemyBuilder:
    def __init__(self, player:Player, colisionHandler, collision_group, sprites_group):
        self.enemy_factory = EnemyFactory(player, colisionHandler, collision_group, sprites_group)
        self.enemy_types = {
            'pink_slime': (PINK_SLIME_SPRITESHEET, PINK_SLIME_SPEED, PINK_SLIME_SCALE, PINK_SLIME_HEALTH, PINK_SLIME_ATTACK_DAMAGE, PINK_SLIME_ATTACK_RANGE, SLIME_WANDER_TIME),
            'blue_slime': (BLUE_SLIME_SPRITESHEET, BLUE_SLIME_SPEED, BLUE_SLIME_SCALE, BLUE_SLIME_HEALTH, BLUE_SLIME_ATTACK_DAMAGE, BLUE_SLIME_ATTACK_RANGE, SLIME_WANDER_TIME),
            'green_slime': (GREEN_SLIME_SPRITESHEET, GREEN_SLIME_SPEED, GREEN_SLIME_SCALE, GREEN_SLIME_HEALTH, GREEN_SLIME_ATTACK_DAMAGE, GREEN_SLIME_ATTACK_RANGE, SLIME_WANDER_TIME),
            'skeleton1':(SKELETON1_SPRITESHEET, SKELETON1_SPEED, SKELETON1_SCALE, SKELETON1_HEALTH, SKELETON1_ATTACK_DAMAGE, SKELETON1_ATTACK_RANGE, SKELETON1_WANDER_TIME)
        }


    def create_enemy(self, enemy_type, x, y):
        if enemy_type in self.enemy_types:
            spritesheet, speed, scale, health, attack_damage, attack_range, wander_time = self.enemy_types[enemy_type]
            return self.enemy_factory(enemy_type, spritesheet, speed, scale, health, attack_damage, attack_range, wander_time, x, y)
        else:
            raise ValueError(f"Unknown enemy type: {enemy_type}")