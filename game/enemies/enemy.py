import pygame
import random

from game.enemies.healthdrop import HealthDrop
from game.sounds.sound_manager import SoundManager
from game.healthbars.enemy_healthbar import EnemyHealthBar
from game.sprites.sprite import Spritesheet
from config.game_settings import get_global_scale, HEALTHBAR_WIDTH, HEALTHDROP_CHANCE, ENEMY_ATTACK_COOLDOWN, \
    ENEMY_SLOW_TIME, \
    ENEMY_SLOW_SPEED, LOAD_TIME, KNOCKBACK_DISTANCE, KNOCKBACK_DURATION
from config.game_settings import ENEMY_DETECTION_RADIUS, ENEMY_LOST_PLAYER_TIME

class Enemy(pygame.sprite.Sprite):
    def __init__(self, spritesheet, colisionHandler, wander_time: int, frame_width:int, frame_height:int, num_frames, x, y, speed, attack_type, attack_damage, attack_range, health, colision_group, sprites_group, enemy_type='default', scale=1, player=None):
        super().__init__(sprites_group)
        self.current_animation = None
        self.animations = None
        self.is_hit = False
        self.direction = None
        self.spritesheet = Spritesheet(spritesheet)
        self.attack_type = attack_type
        self.enemy_type = enemy_type
        self.scale = scale
        self.player = player
        self.sound_manager = SoundManager()
        self.max_speed = speed
        self.collision_group = colision_group
        self.speed = speed
        self.sprites_group = sprites_group
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
        self.damage_timer = 0  # Timer for damage color
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.is_recolored= False
        self.last_attack_time = 0
        self.health_bar = EnemyHealthBar(x, y, (frame_width * scale) // 2, (frame_height * scale) // 5, health, self.sprites_group)
        self.isWaiting = False
        self.type = 'enemy'
        self.health_bar_pos = (x, y)
        self.creation_time = pygame.time.get_ticks()
        self.knockback_velocity = pygame.math.Vector2(0, 0)
        self.knockback_duration = 0

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
            self.image = self.frames[self.current_frame]
            self.current_frame = (self.current_frame + 1) % len(self.frames)

    def move_towards(self, x, y, delta_time):
        self.previous_position = self.rect.topleft  # Store the previous position
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

    def draw(self, screen,):
        # Adjust the enemy's position by the camera offset
        screen.blit(self.image, self.rect)

    def update(self, delta_time):
        player_pos = self.player.get_position()
        previous_pos = self.rect.topleft
        if self.done_moving_slow():
            self.speed = self.max_speed
        if not self.is_hit:
            in_range = self.check_in_range()
            in_detection_radius = self.direction.length() < ENEMY_DETECTION_RADIUS
            in_site = False
            if in_detection_radius:
                in_site = self.has_line_of_sight(player_pos)
            in_time = pygame.time.get_ticks() - self.lastSeenPlayer < ENEMY_LOST_PLAYER_TIME

            if in_range or (in_detection_radius and in_site) or in_time:
                if in_site and in_detection_radius:
                    self.lastSeenPlayer = pygame.time.get_ticks()
                self.move_towards(*player_pos, delta_time)
                if self.check_in_range():
                    self.deal_damage()
            else:
                self.wander(delta_time)
        else:
            self.take_knockback(delta_time)
        self.health_bar.update_details(*self.health_bar_pos, self.health)
        self.update_animation(delta_time)

        # Check for collisions with the tiles
        if any(self.rect.colliderect(tile.rect) for tile in self.collision_group):
            # Handle the collision (e.g., stop movement, revert position, etc.)
            self.rect.topleft = previous_pos

        # Reset color after damage timer expires
        if self.is_recolored and pygame.time.get_ticks() - self.damage_timer > 100:  # Reset after 100 ms
            self.reset_color()

    def kill(self):
        self.player.add_kill()
        self.health_bar.update_details(self.rect.centerx, self.rect.centery, 0)
        self.drop_health()
        super().kill()

    def take_damage(self, damage):
        self.health -= damage
        self.recolor((255, 0, 0))  # Recolor to red when taking damage
        self.damage_timer = pygame.time.get_ticks()  # Record the time of damage
        self.is_recolored = True  # Set recolored flag
        self.is_hit = True
        self.sound_manager.play_sound('enemy_hit')
        self.start_knockback()
        if self.health <= 0:
            self.kill()

    def deal_damage(self):
        if pygame.time.get_ticks() - self.last_attack_time > ENEMY_ATTACK_COOLDOWN:
            self.player.take_damage(self.attack_damage)
            self.last_attack_time = pygame.time.get_ticks()
            self.speed = ENEMY_SLOW_SPEED
            self.sound_manager.play_sound('enemy_attack')

    def get_position(self):
        return self.rect.center

    def recolor(self, color):
        self.image = self.frames[self.current_frame].copy()
        self.image.fill(color, special_flags=pygame.BLEND_MULT)
        self.is_recolored = True

    def reset_color(self):
        self.image = self.frames[self.current_frame]
        self.is_recolored= False

    def done_moving_slow(self):
        return pygame.time.get_ticks() - self.last_attack_time > ENEMY_SLOW_TIME

    def drop_health(self):
        if random.random() < HEALTHDROP_CHANCE:  # 20% chance to drop health
            health_drop = HealthDrop(self.rect.centerx, self.rect.centery, 20, self.sprites_group)
            self.sprites_group.add(health_drop)  # Add to the same group as the enemy

    #Makes sure that the enemies arent moving while the level is loading
    def can_update(self):
        return pygame.time.get_ticks() - self.creation_time > LOAD_TIME  # Wait 1 second before updating the enemy

    #We need to decide if we want to use this function or not
    def take_knockback(self, delta_time):
        if self.knockback_duration > 0:
            self.rect.center += self.knockback_velocity * delta_time
            self.knockback_duration -= delta_time
            if self.knockback_duration <= 0:
                self.knockback_velocity = pygame.math.Vector2(0, 0)
        else:
            self.is_hit = False

    def start_knockback(self):
        player_pos = pygame.math.Vector2(self.player.get_position())
        enemy_pos = pygame.math.Vector2(self.rect.center)
        knockback_direction = (enemy_pos - player_pos).normalize()
        self.knockback_velocity = knockback_direction * KNOCKBACK_DISTANCE
        self.knockback_duration = KNOCKBACK_DURATION  # Duration of the knockback in seconds

    def has_line_of_sight(self, target_pos, step_size=10):
        return True
        current_pos = pygame.math.Vector2(self.rect.center)
        target_pos = pygame.math.Vector2(target_pos)

        x0, y0 = int(current_pos.x), int(current_pos.y)
        x1, y1 = int(target_pos.x), int(target_pos.y)

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy

        while True:
            if any(tile.rect.collidepoint((x0, y0)) for tile in self.collision_group):
                return False
            if x0 == x1 and y0 == y1:
                break
            e2 = err * 2
            if e2 > -dy:
                err -= dy
                x0 += sx * step_size
            if e2 < dx:
                err += dx
                y0 += sy * step_size

        return True