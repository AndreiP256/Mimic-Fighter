from config.game_settings import FLAME_PROJECTLE_PATH
from game.enemies.enemy import Enemy
from game.enemies.monster_pack_enemy import FlameSkullEnemy
from game.enemies.skeleton_enemy import SkeletonEnemy
from game.enemies.slime_enemy import SlimeEnemy


class EnemyFactory:
    def __init__(self, player, colisionHandler, collision_group, sprites_group):
        self.player = player
        self.collision_group = collision_group
        self.colisionHandler = colisionHandler
        self.sprites_group = sprites_group
        pass
    def __call__(self, type : str, spritesheet, speed, scale, health, attack_damage, attack_range, wander_time, x, y) -> Enemy:
        if 'slime' in type:
            return SlimeEnemy(sprites_group = self.sprites_group, spritesheet=spritesheet, wander_time=wander_time,
                              colisionHandler=self.colisionHandler, frame_width=32, frame_height=32, attack_damage=attack_damage, attack_range=attack_range, num_frames=4, x=x, y=y, speed=speed, attack_type='melee', scale=scale, health=health, player = self.player, colision_group= self.collision_group)
        if 'skeleton' in type:
            return SkeletonEnemy(sprites_group = self.sprites_group, spritesheet=spritesheet, wander_time=wander_time,
                              colisionHandler=self.colisionHandler, frame_width=16, frame_height=16, attack_damage=attack_damage, attack_range=attack_range, num_frames=4, x=x, y=y, speed=speed, attack_type='melee', scale=scale, health=health, player = self.player, colision_group= self.collision_group)
        if type == 'flame_skull':
            return FlameSkullEnemy(sprites_group = self.sprites_group, spritesheet=spritesheet, wander_time=wander_time,
                              colisionHandler=self.colisionHandler, frame_width=16, frame_height=16, attack_damage=attack_damage, attack_range=attack_range, num_frames=4, x=x, y=y, speed=speed, attack_type='ranged', scale=scale, health=health, player = self.player, colision_group= self.collision_group, projectile_path=FLAME_PROJECTLE_PATH)
        raise ValueError(f"Unknown enemy type: {type}")