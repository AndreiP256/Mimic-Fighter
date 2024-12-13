
import pygame
from game.enemies.enemy import Enemy
from game.sprites.sprite import Spritesheet


class FlameSkullEnemy(Enemy):
    def __init__(self, spritesheet, frame_width, colisionHandler, wander_time, frame_height, num_frames, x, y, speed, attack_type, health, attack_damage, attack_range, colision_group, sprites_group, enemy_group, scale=1, player=None, projectile_path=None, projectile_cooldown=1000):
        super().__init__(spritesheet=spritesheet, sprites_group=sprites_group, colisionHandler= colisionHandler, wander_time=wander_time, frame_width=frame_width, health=health, frame_height=frame_height, num_frames=num_frames, x=x, y=y, speed=speed, attack_damage=attack_damage, attack_range= attack_range, attack_type=attack_type, enemy_type='ranged', scale=scale,
                         player=player, colision_group=colision_group, projectile_path=projectile_path, projectile_cooldown=projectile_cooldown, enemy_group=enemy_group)

        ## define slime specific animations
        self.animations = {
            'right': self.load_frames(frame_width, frame_height, num_frames, row=0),
            'left': self.load_frames(frame_width, frame_height, num_frames, row=1),
            'down': self.load_frames(frame_width, frame_height, num_frames, row=2),
            'up': self.load_frames(frame_width, frame_height, num_frames, row=3)
        }
        self.current_animation = 'right'
        self.frames = self.animations[self.current_animation]
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_frect()
        self.collision_rect = pygame.FRect(0, 0, int(self.rect.width * 0.3), int(self.rect.height * 0.25))
        self.rect.center = (x, y)
        self.collision_rect.center = self.rect.center

    def set_animation_based_on_direction(self, direction):
        if abs(direction.x) > abs(direction.y):
            if direction.x > 0:
                self.set_animation('right')
            else:
                self.set_animation('left')
        else:
            if direction.y > 0:
                self.set_animation('down')
            else:
                self.set_animation('up')

    def update(self, delta_time):
        self.health_bar_pos = self.rect.center
        super().update(delta_time)
        self.update_animation(delta_time)
        self.set_animation_based_on_direction(self.direction)