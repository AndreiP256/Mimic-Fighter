
import pygame
from game.enemies.enemy import Enemy
from game.sprites.sprite import Spritesheet


class SlimeEnemy(Enemy):
    def __init__(self, spritesheet, frame_width, colisionHandler, wander_time, frame_height, num_frames, x, y, speed, attack_type, health, attack_damage, attack_range, colision_group, sprites_group, scale=1, player=None):
        super().__init__(spritesheet=spritesheet, sprites_group=sprites_group, colisionHandler= colisionHandler, wander_time=wander_time, frame_width=frame_width, health=health, frame_height=frame_height, num_frames=num_frames, x=x, y=y, speed=speed, attack_damage=attack_damage, attack_range= attack_range, attack_type=attack_type, enemy_type='slime', scale=scale,
                         player=player, colision_group=colision_group)

        ## define slime specific animations
        self.animations = {
            'idle': self.load_frames(frame_width, frame_height, num_frames, row=0),
            'left': self.load_frames(frame_width, frame_height, num_frames, row=1),
            'right': self.load_frames(frame_width, frame_height, num_frames, row=1, flip=True),
            'back': self.load_frames(frame_width, frame_height, num_frames, row=2)
        }
        self.current_animation = 'idle'
        self.frames = self.animations[self.current_animation]
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.collision_rect = pygame.Rect(0, 0, int(self.rect.width * 0.3), int(self.rect.height * 0.25))
        self.collision_rect.center = self.rect.center
        self.rect.topleft = (x, y)

    def set_animation_based_on_direction(self, direction):
        if abs(direction.x) > abs(direction.y):
            if direction.x > 0:
                self.set_animation('right')
            else:
                self.set_animation('left')
        else:
            if direction.y > 0:
                self.set_animation('idle')
            else:
                self.set_animation('back')

    def update(self, delta_time):
        super().update(delta_time)
        self.update_animation(delta_time)
        self.set_animation_based_on_direction(self.direction)