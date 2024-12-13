from config.game_settings import FLAME_PROJECTLE_PATH, BLUE_PROJECTLE_PATH, MOMO_PROJECTILE_PATH, \
    FLAME_SKULL_PROJECTILE_COOLDOWN, BLUE_SKULL_PROJECTILE_COOLDOWN
from game.enemies.enemy import Enemy
from game.enemies.monster_pack_enemy import FlameSkullEnemy
from game.enemies.skeleton_enemy import SkeletonEnemy
from game.enemies.slime_enemy import SlimeEnemy
from game.enemies.momo_mama import MomoMama


class EnemyFactory:
    def __init__(self, player, colisionHandler, collision_group, sprites_group, enemy_group):
        self.player = player
        self.collision_group = collision_group
        self.colisionHandler = colisionHandler
        self.sprites_group = sprites_group
        self.enemy_group = enemy_group
        pass
    def __call__(self, type : str, spritesheet, speed, scale, health, attack_damage, attack_range, wander_time, x, y, enemy_builder = None) -> Enemy:
        if 'slime' in type:
            return SlimeEnemy(sprites_group = self.sprites_group, spritesheet=spritesheet, wander_time=wander_time,
                              colisionHandler=self.colisionHandler, frame_width=32, frame_height=32, attack_damage=attack_damage, attack_range=attack_range, num_frames=4, x=x, y=y, speed=speed, attack_type='melee', scale=scale, health=health, player = self.player, colision_group= self.collision_group, enemy_group=self.enemy_group)
        if 'skeleton' in type:
            return SkeletonEnemy(sprites_group = self.sprites_group, spritesheet=spritesheet, wander_time=wander_time,
                              colisionHandler=self.colisionHandler, frame_width=16, frame_height=16, attack_damage=attack_damage, attack_range=attack_range, num_frames=4, x=x, y=y, speed=speed, attack_type='melee', scale=scale, health=health, player = self.player, colision_group= self.collision_group, enemy_group=self.enemy_group)
        if type == 'flame_skull':
            return FlameSkullEnemy(sprites_group = self.sprites_group, spritesheet=spritesheet, wander_time=wander_time,
                              colisionHandler=self.colisionHandler, frame_width=16, frame_height=16, attack_damage=attack_damage, attack_range=attack_range, num_frames=4, x=x, y=y, speed=speed, attack_type='ranged', scale=scale, health=health, player = self.player, colision_group= self.collision_group, projectile_path=FLAME_PROJECTLE_PATH, projectile_cooldown=FLAME_SKULL_PROJECTILE_COOLDOWN, enemy_group=self.enemy_group)
        if type == 'blue_skull':
            return FlameSkullEnemy(sprites_group = self.sprites_group, spritesheet=spritesheet, wander_time=wander_time,
                              colisionHandler=self.colisionHandler, frame_width=16, frame_height=16, attack_damage=attack_damage, attack_range=attack_range, num_frames=4, x=x, y=y, speed=speed, attack_type='ranged', scale=scale, health=health, player = self.player, colision_group= self.collision_group, projectile_path=BLUE_PROJECTLE_PATH, projectile_cooldown=BLUE_SKULL_PROJECTILE_COOLDOWN, enemy_group=self.enemy_group)
        if type == 'momo_mama':
            return MomoMama(sprites_group = self.sprites_group, spritesheet=spritesheet, wander_time=wander_time, colisionHandler=self.colisionHandler, frame_width=64, frame_height=64, attack_damage=attack_damage, attack_range=attack_range, num_frames=4, x=x, y=y, speed=speed, attack_type='melee', scale=scale, health=health, player = self.player, colision_group= self.collision_group, projectile_path=MOMO_PROJECTILE_PATH,
                            enemy_builder=enemy_builder, enemy_group=self.enemy_group)
        raise ValueError(f"Unknown enemy type: {type}")