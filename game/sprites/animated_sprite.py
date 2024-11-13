import pygame
from game.sprites.sprite import Spritesheet

class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, spritesheet, frame_width, frame_height, num_frames, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.spritesheet = Spritesheet(spritesheet)
        self.frames = self.load_frames(frame_width, frame_height, num_frames)
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = speed
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100  # Time in milliseconds between frames

    def load_frames(self, frame_width: int, frame_height: int, num_frames: int, row: int, flip=False) -> list:
        frames = []
        for i in range(num_frames):
            x = i * frame_width
            y = 0
            frames.append(self.spritesheet.get_image(x, y, frame_width, frame_height))
        return frames

    def update(self, *args, **kwargs):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]