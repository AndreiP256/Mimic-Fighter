from game.sprites.sprite import Spritesheet
import pygame
from game.enemies.enemy import Enemy
from config.game_settings import MOMO_HEALTH_Y, MOMO_HEALTH_X, MOMO_HEALTHBAR_HEIGHT, MOMO_HEALTHBAR_WIDTH
from game.healthbars.boss_bar import BossBar
class MomoMama(Enemy):
    def __init__(self, spritesheet, frame_width, colisionHandler, wander_time, frame_height, num_frames, x, y, speed, attack_type, health, attack_damage, attack_range, colision_group, sprites_group, scale=1, player=None, projectile_path=None):
        self.type = 'boss'
        super().__init__(spritesheet=spritesheet, sprites_group=sprites_group, colisionHandler= colisionHandler, wander_time=wander_time, frame_width=frame_width, health=health, frame_height=frame_height, num_frames=num_frames, x=x, y=y, speed=speed, attack_damage=attack_damage, attack_range= attack_range, attack_type=attack_type, enemy_type='ranged', scale=scale,
                         player=player, colision_group=colision_group, projectile_path=projectile_path, projectile_cooldown=1000, type='boss')

        ## define slime specific animations
        self.is_jumping = False
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
        self.last_jump_time = pygame.time.get_ticks()
        self.set_animation_based_on_direction(pygame.Vector2(0,0), 'crawl')

    def update(self, delta_time):
        previous_position = self.rect.topleft
        self.health_bar_pos = self.rect.center
        self.direction = pygame.math.Vector2(self.player.rect.center) - pygame.math.Vector2(self.rect.center)
        # if self.can_spawn_slime():
        #     self.spawn_slime()
        # elif self.player.can_ranged_attack(self):
        #     self.doNormalAttack()
        # elif self.player.can_melee_attack(self):
        #     self.doRangedAttack()
        if True:
            if self.can_jump():
                self.jump(self.player.rect.center, delta_time)
            if not self.is_jumping:
                self.set_animation_based_on_direction(self.direction, 'crawl')
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


    def jump(self, player_pos, delta_time):
        direction = pygame.math.Vector2(player_pos) - pygame.math.Vector2(self.rect.center)
        if direction.length() > 0:
            direction = direction.normalize()
        self.set_animation_based_on_direction(direction, 'jump')
        self.speed = self.max_speed * 6
        self.is_jumping = True

    def can_jump(self):
        return (pygame.time.get_ticks() - self.last_jump_time) > 5000 and not self.is_jumping

    def update_animation(self, delta_time):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.image = self.frames[self.current_frame]
            self.current_frame = (self.current_frame + 1) % len(self.frames)
        if 'jump' in self.current_animation and self.current_frame == len(self.frames) - 1:
            self.is_jumping = False
            self.speed = self.max_speed
            self.last_jump_time = now

