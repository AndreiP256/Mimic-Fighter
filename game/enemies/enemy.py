import random
import pygame
from game.sprites.animated_sprite import AnimatedSprite
from game.sprites.sprite import Spritesheet
from config.game_settings import get_global_scale
from game.player.player import Player
from game.sprites.colision_handler import ColisionHandler
from config.game_settings import ENEMY_DETECTION_RADIUS, ENEMY_LOST_PLAYER_TIME

class Enemy(AnimatedSprite):
    def __init__(self, spritesheet, colisionHandler, wander_time: int, frame_width, frame_height, num_frames, x, y, speed, attack_type, attack_damage, attack_range, health, enemy_type='default', scale=1, player=None):
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
        self.health = health
        self.attack_damage = attack_damage
        self.attack_range = attack_range
        self.colisionHandler = colisionHandler
        self.wander_time = wander_time
        self.c_wander_time = pygame.time.get_ticks()
        self.wander_direction = pygame.math.Vector2(0, 0)
        self.lastSeenPlayer = 0

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

    def move_randomly(self, delta_time):
        random_direction = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
        self.rect.center += random_direction * self.speed * delta_time * 0.2

    def wander(self, delta_time):
        if pygame.time.get_ticks() - self.c_wander_time > self.wander_time:  # Change direction every 2 seconds
            self.c_wander_time = pygame.time.get_ticks()
            self.wander_direction = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
        self.rect.center += self.wander_direction * self.speed * delta_time * 0.1

    def check_in_range(self):
        target_pos = pygame.math.Vector2(*self.player.get_position())
        current_pos = pygame.math.Vector2(self.rect.center)
        self.direction = target_pos - current_pos
        return self.direction.length() < self.attack_range

    def update(self, delta_time):
        player_pos = self.player.get_position()
        if self.check_in_range() or self.direction.length() < ENEMY_DETECTION_RADIUS or self.lastSeenPlayer < ENEMY_LOST_PLAYER_TIME:
            self.lastSeenPlayer = pygame.time.get_ticks()
            self.move_towards(*player_pos, delta_time)
            if self.check_in_range():
                self.deal_damage()
        else:
            self.wander(delta_time)
        self.update_animation(delta_time)

    def kill(self):
        super().kill()

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()

    def deal_damage(self):
        self.player.take_damage(self.attack_damage)

    def get_position(self):
        return self.rect.center
