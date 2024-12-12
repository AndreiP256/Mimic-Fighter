from game.sprites.projectiles.enemy_projectile import EnemyProjectile
from game.sprites.sprite import Spritesheet
import pygame
import math
from game.enemies.enemy import Enemy
from config.game_settings import MOMO_HEALTH_Y, MOMO_HEALTH_X, MOMO_HEALTHBAR_HEIGHT, MOMO_HEALTHBAR_WIDTH, \
    MOMO_RANGED_COOLDOWN, MOMO_PROJECTILE_PATH, MOMO_NUM_PROJECTILES, MOMO_MAMA_ATTACK_RANGE, MOMO_MAMA_ATTACK_DAMAGE, \
    MOMO_MELEE_COOLDOWN, MOMO_JUMP_COOLDOWN, MOMO_SPAWN_COOLDOWN
from game.healthbars.boss_bar import BossBar
class MomoMama(Enemy):
    def __init__(self, spritesheet, frame_width, colisionHandler, wander_time, frame_height, num_frames, x, y, speed, attack_type, health, attack_damage, attack_range, colision_group, sprites_group, scale=1, player=None, projectile_path=None, enemy_builder=None):
        self.is_spawning_slimes = None
        self.last_spawn_time = 0
        self.enemy_builder = enemy_builder
        self.is_taking_damage = False
        self.projectile_speed = None
        self.projectile_damage = None
        self.last_ranged_attack = 0
        self.type = 'boss'
        super().__init__(spritesheet=spritesheet, sprites_group=sprites_group, colisionHandler= colisionHandler, wander_time=wander_time, frame_width=frame_width, health=health, frame_height=frame_height, num_frames=num_frames, x=x, y=y, speed=speed, attack_damage=attack_damage, attack_range= attack_range, attack_type=attack_type, enemy_type='ranged', scale=scale,
                         player=player, colision_group=colision_group, projectile_path=projectile_path, projectile_cooldown=1000, type='boss')

        ## define slime specific animations
        self.is_jumping = False
        self.is_ranged_attacking = False
        self.animations = {
            'down_chomp': self.load_frames(frame_width, frame_height, 6, row=0),
            'left_chomp': self.load_frames(frame_width, frame_height, 6, row=1),
            'right_chomp': self.load_frames(frame_width, frame_height, 6, row=1, flip=True),
            'up_chomp': self.load_frames(frame_width, frame_height, 6, row=2),
            'down_crawl': self.load_frames(frame_width, frame_height, 5, row=3),
            'left_crawl': self.load_frames(frame_width, frame_height, 5, row=4),
            'right_crawl': self.load_frames(frame_width, frame_height, 5, row=4, flip=True),
            'up_crawl': self.load_frames(frame_width, frame_height, 5, row=5),
            'down_generic': self.load_frames(frame_width, frame_height, 7, row=6),
            'left_generic': self.load_frames(frame_width, frame_height, 7, row=7),
            'right_generic': self.load_frames(frame_width, frame_height, 7, row=7, flip=True),
            'up_generic': self.load_frames(frame_width, frame_height, 7, row=8),
            'down_hurt': self.load_frames(frame_width, frame_height, 6, row=9),
            'left_hurt': self.load_frames(frame_width, frame_height, 6, row=10),
            'right_hurt': self.load_frames(frame_width, frame_height, 6, row=10, flip=True),
            'up_hurt': self.load_frames(frame_width, frame_height, 6, row=11),
            'down_jump': self.load_frames(frame_width, frame_height, 6 ,row=12),
            'left_jump': self.load_frames(frame_width, frame_height, 6, row=13),
            'right_jump': self.load_frames(frame_width, frame_height, 6, row=13, flip=True),
            'up_jump': self.load_frames(frame_width, frame_height, 6, row=14),
            'spin': self.load_frames(frame_width, frame_height, 4, row=15),
            'spin_fx': self.load_frames(frame_width, frame_height, 4, row=16),
        }

        self.health_bar = BossBar(MOMO_HEALTH_X, MOMO_HEALTH_Y, MOMO_HEALTHBAR_WIDTH, MOMO_HEALTHBAR_HEIGHT, self.health)
        self.current_animation = 'down_crawl'
        self.frames = self.animations[self.current_animation]
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_frect()
        self.collision_rect = pygame.FRect(0, 0, int(self.rect.width * 0.3), int(self.rect.height * 0.25))
        self.rect.center = (x, y)
        self.collision_rect.center = self.rect.center
        self.is_normal_attacking = False
        self.last_jump_time = pygame.time.get_ticks()
        self.set_animation_based_on_direction(pygame.Vector2(0,0), 'crawl')
        self.projectile_image = pygame.image.load(MOMO_PROJECTILE_PATH).convert_alpha()

    def update(self, delta_time):
        previous_position = self.rect.topleft
        self.health_bar_pos = self.rect.center
        self.health_bar.update_details(self.health)
        self.direction = pygame.math.Vector2(self.player.rect.center) - pygame.math.Vector2(self.rect.center)
        if not self.is_taking_damage:
            if self.can_spawn_slime():
                self.set_animation('spin')
                self.spawn_slime()
            elif self.can_ranged_attack():
                self.set_animation('spin_fx')
                self.do_ranged_attack()
            elif self.can_melee_attack():
                self.do_melee_attack()
            elif self.can_move():
                if self.can_jump():
                    self.jump(self.player.rect.center)
                if not self.is_jumping:
                    self.set_animation_based_on_direction(self.direction, 'crawl')
                if not self.player_in_range():
                    self.move_towards(*self.player.rect.center, delta_time)
        self.update_animation(delta_time)
        if any(self.rect.colliderect(tile.rect) for tile in self.collision_group):
            self.rect.topleft = previous_position

    def set_animation_based_on_direction(self, direction, animation):
        if abs(direction.x) > abs(direction.y):
            if direction.x > 0:
                self.set_animation('right_' + animation)
            else:
                self.set_animation('left_' + animation)
        else:
            if direction.y > 0:
                self.set_animation('down_' + animation)
            else:
                self.set_animation('up_' + animation)


    def jump(self, player_pos):
        direction = pygame.math.Vector2(player_pos) - pygame.math.Vector2(self.rect.center)
        if direction.length() > 0:
            direction = direction.normalize()
        self.set_animation_based_on_direction(direction, 'jump')
        self.speed = self.max_speed * 6
        self.is_jumping = True

    def can_jump(self):
        return (pygame.time.get_ticks() - self.last_jump_time) > MOMO_JUMP_COOLDOWN and not self.is_jumping

    def update_animation(self, delta_time):
        print(self.is_normal_attacking)
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.image = self.frames[self.current_frame]
            self.current_frame = (self.current_frame + 1) % len(self.frames)
        if "jump" in self.current_animation and self.current_frame == 5:
            self.is_jumping = False
            self.speed = self.max_speed
            self.last_jump_time = now
        if "chomp" in self.current_animation and self.current_frame == 5:
            self.speed = self.max_speed
            self.is_normal_attacking = False
            self.last_attack_time = now
        if "hurt" in self.current_animation and self.current_frame == 5:
            self.reset_state(now)
        if 'spin_fx' in self.current_animation and self.current_frame == 3:
            self.is_ranged_attacking = False
            self.last_ranged_attack = now
        if self.current_animation  == 'spin' and self.current_frame == 3:
            self.is_spawning_slimes = False
            self.last_spawn_time = now

    def can_melee_attack(self):
        if self.is_attacking() or pygame.time.get_ticks() - self.last_attack_time < MOMO_MELEE_COOLDOWN:
            return False
        if self.is_jumping:
            return False
        return self.player_in_range()

    def do_melee_attack(self):
        self.set_animation_based_on_direction(self.direction, 'chomp')
        self.player.take_damage(MOMO_MAMA_ATTACK_DAMAGE)
        self.is_normal_attacking = True

    def take_damage(self, damage):
        if not self.is_taking_damage:
            self.health -= damage
            self.set_animation_based_on_direction(self.direction, 'hurt')
            self.is_taking_damage = True
            self.is_hit = True
            self.sound_manager.play_sound('enemy_hit')
            if self.health <= 0:
                self.kill()

    def do_ranged_attack(self):
        self.last_ranged_attack = pygame.time.get_ticks()
        self.is_ranged_attacking = True
        angle_step = 360 / MOMO_NUM_PROJECTILES  # Angle between each projectile

        for i in range(MOMO_NUM_PROJECTILES):
            angle = math.radians(i * angle_step)
            direction = pygame.math.Vector2(math.cos(angle), math.sin(angle))
            self.spawn_projectile(direction)

    def spawn_projectile(self, direction):
        EnemyProjectile(self.projectile_image, self.rect.center, direction, self.sprites_group, self.player,
                        self.attack_damage, self.collision_group, 3)


    def can_ranged_attack(self):
        return pygame.time.get_ticks() - self.last_ranged_attack > MOMO_RANGED_COOLDOWN and not self.is_jumping

    def can_move(self):
        return not self.is_attacking()

    def reset_state(self, now):
        self.is_taking_damage = False
        self.is_normal_attacking = False
        self.is_ranged_attacking = False
        self.is_spawning_slimes = False
        self.is_jumping = False
        self.speed = self.max_speed
        self.set_animation_based_on_direction(self.direction, 'crawl')
        self.last_jump_time = now

    def can_spawn_slime(self):
        return pygame.time.get_ticks() - self.last_spawn_time > MOMO_SPAWN_COOLDOWN and not self.is_jumping

    def spawn_slime(self):
        self.last_spawn_time = pygame.time.get_ticks()
        self.is_spawning_slimes = True
        corners = [
            (self.rect.left, self.rect.top),
            (self.rect.right, self.rect.top),
            (self.rect.left, self.rect.bottom),
            (self.rect.right, self.rect.bottom)
        ]

        # Spawn a slime at each corner
        for corner in corners:
            enemy = self.enemy_builder.create_enemy('pink_slime', corner[0], corner[1])
            self.colisionHandler.add_enemy(enemy)


    def is_attacking(self):
        return self.is_normal_attacking or self.is_ranged_attacking or self.is_spawning_slimes

    def player_in_range(self):
        target_pos = pygame.math.Vector2(*self.player.get_position())
        current_pos = pygame.math.Vector2(self.rect.center)
        self.direction = target_pos - current_pos
        return self.direction.length() < MOMO_MAMA_ATTACK_RANGE
