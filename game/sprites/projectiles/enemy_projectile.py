import pygame

from game.sprites.projectiles.projectile import Projectile


class EnemyProjectile(Projectile):
    def __init__(self, surf, pos, direction, groups, player, damage, collision_group):
        super().__init__(surf, pos, direction, groups, collision_group)
        self.player = player
        self.damage = damage

    def update(self, dt):
        super().update(dt)
        if self.rect.colliderect(self.player.collision_rect):
            if self.player.take_damage(self.damage):
                self.kill()