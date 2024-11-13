
import pygame
from game.enemies.enemy import Enemy
from game.sprites.sprite import Spritesheet


class SlimeEnemy(Enemy):
    def __init__(self, spritesheet, frame_width, frame_height, num_frames, x, y, speed, attack_type, scale=1, player=None):
        super().__init__(spritesheet, frame_width, frame_height, num_frames, x, y, speed, attack_type, 'slime', scale,
                         player)

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