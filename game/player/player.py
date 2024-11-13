# game/player.py
import string

import pygame

from game.sprites.animated_sprite import AnimatedSprite
from game.sprites.sprite import Spritesheet


class Player(AnimatedSprite):
    def __init__(self, spritesheet, frame_width: int, frame_height: int, x: int, y: int, speed: int,
                 scale: object = 1, frame_rate: int = 30, health: object = 100, attack_power: object = 10):
        pygame.sprite.Sprite.__init__(self)
        self.direction = None
        self.spritesheet = Spritesheet(spritesheet)
        self.scale = scale
        self.speed = speed
        self.health = health
        self.attack_power = attack_power
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = frame_rate
        self.animations = {
            'idle': self.load_frames(frame_width, frame_height, 12, row=0),   # Row 0: 12 frames for 'idle'
            'move_down': self.load_frames(64, 65, 8, row=1),            # Row 1: 8 frames for 'move_right'
            'run_down': self.load_frames(64, 65, 8, row=2),             # Row 2: 8 frames for 'move_left'
            'chop_down': self.load_frames(64, 65, 4, row=3),                  # Row 3: 4 frames for 'jump'
            'slash_down': self.load_frames(64, 65, 7, row=4),                  # Row 4: 7 frames for 'fall'
            'roll_down': self.load_frames(64, 65, 8, row=5),  # Add frame count for 'attack_right'
            'idle_right': self.load_frames(64, 65, 12, row=6),   # Add frame count for 'attack_left'
            'move_right': self.load_frames(64, 65, 8, row=7),          # Add frame count for 'hurt'
            'run_right': self.load_frames(64, 65, 8, row=8),           # Add frame count for 'die'
            'chop_right': self.load_frames(64, 65, 4, row=9),     # Add frame count for 'celebrate'
            'slash_right': self.load_frames(64, 65, 7, row=10),        # Add frame count for 'slide'
            'roll_right': self.load_frames(64, 65, 8, row=11),       # Add frame count for 'crouch'
            'idle_up': self.load_frames(64, 65, 12, row=12),    # Add frame count for 'run_right'
            'move_up': self.load_frames(64, 65, 8, row=13),
            'run_up': self.load_frames(frame_width, frame_height, 8, row=14),  # Row 0: 12 frames for 'idle'
            'chop_up': self.load_frames(64, 65, 4, row=15),  # Row 1: 8 frames for 'move_right'
            'slash_up': self.load_frames(64, 65, 7, row=16),  # Row 2: 8 frames for 'move_left'
            'roll_up': self.load_frames(64, 65, 8, row=17),  # Row 3: 4 frames for 'jump'
            'idle_left': self.load_frames(64, 65, 12, row=6, flip=True),  # Add frame count for 'attack_left'
            'move_left': self.load_frames(64, 65, 8, row=7, flip=True),  # Add frame count for 'hurt'
            'run_left': self.load_frames(64, 65, 8, row=8, flip=True),  # Add frame count for 'die'
            'chop_left': self.load_frames(64, 65, 4, row=9, flip=True),  # Add frame count for 'celebrate'
            'slash_left': self.load_frames(64, 65, 7, row=10, flip=True),  # Add frame count for 'slide'
            'roll_left': self.load_frames(64, 65, 8, row=11, flip=True),  # Add frame count for 'crouch'
            # Add frame count for 'run_left'
        }
        self.current_animation = 'idle'
        self.frames = self.animations[self.current_animation]
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.prevDirection : string = None
        self.direction : string = None

    def update_animation(self, delta_time):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
        if self.current_animation == 'hurt' and self.current_frame == len(self.frames) - 1:
            self.set_animation('idle')


    def update(self, delta_time : float):
        if self.direction == 'right':
            self.rect.x += self.speed * delta_time
            self.set_animation('move_right')
        elif self.direction == 'left':
            self.rect.x -= self.speed * delta_time
            self.set_animation('move_left')
        elif self.direction == 'up':
            self.rect.y -= self.speed * delta_time
            self.set_animation('move_up')
        elif self.direction == 'down':
            self.rect.y += self.speed * delta_time
            self.set_animation('move_down')
        elif self.direction == 'up_right':
            self.rect.x += self.speed * delta_time
            self.rect.y -= self.speed * delta_time
            self.set_animation('move_right')
        elif self.direction == 'up_left':
            self.rect.x -= self.speed * delta_time
            self.rect.y -= self.speed * delta_time
            self.set_animation('move_left')
        elif self.direction == 'down_right':
            self.rect.x += self.speed * delta_time
            self.rect.y += self.speed * delta_time
            self.set_animation('move_right')
        elif self.direction == 'down_left':
            self.rect.x -= self.speed * delta_time
            self.rect.y += self.speed * delta_time
            self.set_animation('move_left')
        else:
            self.set_animation('idle')
        self.prevDirection = self.direction

        self.update_animation(delta_time)

    def get_position(self):
        return self.rect.center

    def load_frames(self, frame_width : int, frame_height : int, num_frames : int, row : int, flip=False) -> list:
        frames = []
        for i in range(num_frames):
            x = i * frame_width
            y = row * frame_height
            frame = self.spritesheet.get_image(x, y, frame_width, frame_height, self.scale)
            if flip:
                frame = pygame.transform.flip(frame, True, False)
            frames.append(frame)
        return frames

    def set_animation(self, animation):
        if animation in self.animations and self.current_animation != animation:
            self.current_animation = animation
            self.frames = self.animations[self.current_animation]
            self.current_frame = 0

    def take_damage(self, damage : int):
        #self.set_animation('hurt')
        self.health -= damage

    def move_right(self):

        if self.direction == 'up':
            self.direction = 'up_right'
        elif self.direction == 'down':
            self.direction = 'down_right'
        elif self.prevDirection is None:
            self.direction = 'right'


    def move_left(self):
        if self.direction == 'up':
            self.direction = 'up_left'
        elif self.direction == 'down':
            self.direction = 'down_left'
        elif self.prevDirection is None:
            self.direction = 'left'

    def move_down(self):
        if self.direction == 'right':
            self.direction = 'down_right'
        elif self.direction == 'left':
            self.direction = 'down_left'
        elif self.direction is None:
            self.direction = 'down'

    def move_up(self):
        if self.direction == 'right':
            self.direction = 'up_right'
        elif self.direction == 'left':
            self.direction = 'up_left'
        elif self.direction is None:
            self.direction = 'up'

    def stop(self):
        self.direction = None

    #def set_animation_based_on_direction(self, direction):