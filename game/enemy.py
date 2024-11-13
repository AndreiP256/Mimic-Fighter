import pygame
from game.sprites.animated_sprite import AnimatedSprite
from game.sprites.sprite import Spritesheet

class Enemy(AnimatedSprite):
    def __init__(self, spritesheet, frame_width, frame_height, num_frames, x, y, speed, attack_type, enemy_type='default', scale=1, player=None):
        pygame.sprite.Sprite.__init__(self)
        self.spritesheet = Spritesheet(spritesheet)
        self.attack_type = attack_type
        self.enemy_type = enemy_type
        self.scale = scale
        self.player = player
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
        direction = target_pos - current_pos
        if direction.length() > 0:
            direction = direction.normalize()
            self.rect.center += direction * self.speed * delta_time
            self.set_animation_based_on_direction(direction)

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
        self.update_animation(delta_time)
        player_pos = self.player.get_position()
        self.move_towards(*player_pos, delta_time)