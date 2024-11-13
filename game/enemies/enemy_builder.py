# enemy_builder.py
from game.enemies.slime_enemy import SlimeEnemy
from config.game_settings import PINK_SLIME_SPRITESHEET, PINK_SLIME_SPEED, PINK_SLIME_SCALE
from config.game_settings import BLUE_SLIME_SPRITESHEET, BLUE_SLIME_SPEED, BLUE_SLIME_SCALE
from config.game_settings import GREEN_SLIME_SPRITESHEET, GREEN_SLIME_SPEED, GREEN_SLIME_SCALE

class EnemyBuilder:
    def __init__(self, player):
        self.player = player
        self.enemy_types = {
            'pink_slime': (PINK_SLIME_SPRITESHEET, PINK_SLIME_SPEED, PINK_SLIME_SCALE),
            'blue_slime': (BLUE_SLIME_SPRITESHEET, BLUE_SLIME_SPEED, BLUE_SLIME_SCALE),
            'green_slime': (GREEN_SLIME_SPRITESHEET, GREEN_SLIME_SPEED, GREEN_SLIME_SCALE)
        }

    def create_enemy(self, enemy_type, x, y):
        if enemy_type in self.enemy_types:
            spritesheet, speed, scale = self.enemy_types[enemy_type]
            return SlimeEnemy(spritesheet, 32, 32, 4, x, y, speed, 'mele', scale, self.player)
        else:
            raise ValueError(f"Unknown enemy type: {enemy_type}")