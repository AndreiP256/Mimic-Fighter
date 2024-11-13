import pygame
from game.sprites.animated_sprite import AnimatedSprite
from game.sprites.sprite import Spritesheet

class Enemy(AnimatedSprite):
    def __init__(self, spritesheet, frame_width, frame_height, num_frames, x, y, speed, attack_type, enemy_type='default', scale=1):
        pygame.sprite.Sprite.__init__(self)
        self.spritesheet = Spritesheet(spritesheet)
        self.attack_type = attack_type
        self.enemy_type = enemy_type
        self.scale = scale
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
        self.speed = speed
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100  # Time in milliseconds between frames

    def load_frames(self, frame_width, frame_height, num_frames, row, flip=False):
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
        if animation in self.animations:
            self.current_animation = animation
            self.frames = self.animations[self.current_animation]
            self.current_frame = 0

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]