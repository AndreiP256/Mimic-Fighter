import pygame
from game.sprites.animated_sprite import AnimatedSprite
from game.sprites.sprite import Spritesheet
from config.game_settings import get_global_scale

class Enemy(AnimatedSprite):
    def __init__(self, spritesheet, frame_width, frame_height, num_frames, x, y, speed, attack_type, enemy_type='default', scale=1, player=None):
        pygame.sprite.Sprite.__init__(self)
        self.direction = None
        self.spritesheet = Spritesheet(spritesheet)
        self.attack_type = attack_type
        self.enemy_type = enemy_type
        self.scale = scale
        self.player = player
        self.speed = speed
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100  # Time in milliseconds between frames

    def load_frames(self, frame_width, frame_height, num_frames, row, flip=False):
        frames = []
        for i in range(num_frames):
            x = i * frame_width
            y = row * frame_height
            frame = self.spritesheet.get_image(x, y, frame_width, frame_height, self.scale * get_global_scale())
            if flip:
                frame = pygame.transform.flip(frame, True, False)
            frames.append(frame)
        return frames

    def set_animation(self, animation):
        if animation in self.animations and self.current_animation != animation:
            self.current_animation = animation
            self.frames = self.animations[self.current_animation]
            self.current_frame = 0

    def update_animation(self, delta_time):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]

    def move_towards(self, x, y, delta_time):
        target_pos = pygame.math.Vector2(x, y)
        current_pos = pygame.math.Vector2(self.rect.center)
        self.direction = target_pos - current_pos
        if self.direction.length() > 0:
            direction = self.direction.normalize()
            self.rect.center += direction * self.speed * delta_time


    def update(self, delta_time):
        player_pos = self.player.get_position()
        self.move_towards(*player_pos, delta_time)