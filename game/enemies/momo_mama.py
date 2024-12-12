from game.sprites.sprite import Spritesheet
import pygame
from game.enemies.enemy import Enemy
class MomoMama(Enemy):
    def __init__(self, spritesheet, frame_width, colisionHandler, wander_time, frame_height, num_frames, x, y, speed, attack_type, health, attack_damage, attack_range, colision_group, sprites_group, scale=1, player=None, projectile_path=None):
        super().__init__(spritesheet=spritesheet, sprites_group=sprites_group, colisionHandler= colisionHandler, wander_time=wander_time, frame_width=frame_width, health=health, frame_height=frame_height, num_frames=num_frames, x=x, y=y, speed=speed, attack_damage=attack_damage, attack_range= attack_range, attack_type=attack_type, enemy_type='ranged', scale=scale,
                         player=player, colision_group=colision_group, projectile_path=projectile_path, projectile_cooldown=1000)

        ## define slime specific animations
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


        self.current_animation = 'down_crawl'
        self.frames = self.animations[self.current_animation]
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_frect()
        self.collision_rect = pygame.FRect(0, 0, int(self.rect.width * 0.3), int(self.rect.height * 0.25))
        self.rect.center = (x, y)
        self.collision_rect.center = self.rect.center

    def update(self, delta_time):
        previous_position = self.rect.topleft
        self.health_bar_pos = self.rect.center
        self.update_animation(delta_time)
        if self.can_spawn_slime():
            self.spawn_slime()
        elif self.player.can_ranged_attack(self):
            self.doNormalAttack()
        elif self.player.can_melee_attack(self):
            self.doRangedAttack()
        else:
            if self.can_jump():
                self.jump(self.player.rect.center, delta_time)
            else:
                self.move_towards(self.player.rect.center, delta_time)
        self.set_animation_based_on_direction(self.direction, 'crawl')
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

