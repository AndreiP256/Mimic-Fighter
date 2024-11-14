# game/player.py
import string
from operator import index

import pygame

from config.game_settings import HERO_SPRINT_MULTIPLIER
from game.sprites.animated_sprite import AnimatedSprite
from game.sprites.sprite import Spritesheet


class Player(AnimatedSprite):
    def __init__(self, spritesheet, frame_width: int, frame_height: int, x: int, y: int, speed: int,
                 scale: object = 1, frame_rate: int = 30, health: object = 100, attack_power: object = 10):
        pygame.sprite.Sprite.__init__(self)
        self.direction = None
        self.spritesheet = Spritesheet(spritesheet)
        self.scale = scale
        self.baseSpeed = speed
        self.speed = speed
        self.health = health
        self.attack_power = attack_power
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = frame_rate
        self.animations = self.load_animations(frame_width, frame_height)
        self.current_animation = 'idle_down'
        self.frames = self.animations[self.current_animation]
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.prevDirection : string = None
        self.direction : string = None
        self.isRunning : bool = False
        self.attack_move = None
        self.isAttacking = False

    def update_animation(self, delta_time):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
        if self.current_animation == 'hurt' and self.current_frame == len(self.frames) - 1:
            self.set_animation('idle_right')

    def load_animations(self, frame_width : int, frame_height : int) -> dict:
        animations = {}
        directions = ['down', 'right', 'up', 'left']
        actions = ['idle', 'move', 'run', 'chop', 'slash', 'roll']
        frame_counts = {
            'idle': 12,
            'move': 8,
            'run': 8,
            'chop': 4,
            'slash': 7,
            'roll': 8
        }
        for i, direction in enumerate(directions):
            for action in actions:
                row = i * len(actions) + actions.index(action)
                if direction == 'left':
                    animations[f'{action}_{direction}'] = [pygame.transform.flip(frame, True, False) for frame in
                                                           animations[f'{action}_right']]
                else:
                    animations[f'{action}_{direction}'] = self.load_frames(frame_width, frame_height,
                                                                           frame_counts[action], row)
        return animations

    def update(self, delta_time : float):
        self.attack()
        self.move(delta_time)
        self.prevDirection = self.direction
        #print("PrevDirection ", self.prevDirection, " Direction", self.direction)
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

    def sprint(self):
        if not self.isRunning:
            self.speed = self.baseSpeed * HERO_SPRINT_MULTIPLIER
        self.isRunning = True

    def stop_sprint(self):
        self.speed = self.baseSpeed
        self.isRunning = False

    def do_chop(self):
        self.attack_move = 'chop'

    def do_slash(self):
        self.attack_move = 'slash'

    def stop_attack(self):
        self.attack_move = 'none'

    def attack(self):
        if self.attack_move is not None:
            if self.prevDirection is None:
                self.set_animation(self.attack_move + '_up')
            else:
                self.set_animation(self.attack_move + '_' + self.prevDirection)
            #implement attack logic
            self.isAttacking = True
            self.attack_move = None

    def move(self, delta_time):
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
        elif self.direction is None and self.prevDirection is not None:
            self.do_idle()
    def do_idle(self):

        if 'right' in self.prevDirection:
            print("Right idle")
            self.set_animation('idle_right')
        elif 'left' in self.prevDirection:
            print("Left idle")
            self.set_animation('idle_left')
        elif self.prevDirection == 'up':
            print("Up idle")
            self.set_animation('idle_up')
        else:
            print("Dowmn idle")
            self.set_animation('idle_down')
