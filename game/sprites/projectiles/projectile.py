import pygame



class Projectile(pygame.sprite.Sprite):
    def __init__(self, surf, pos, direction, groups, collision_group):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center=pos)
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 100000
        self.direction = direction
        self.collison_group = collision_group
        self.speed = 250

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.spawn_time >= self.lifetime:
            self.kill()
        if any(self.rect.colliderect(tile.rect) for tile in self.collison_group):
            self.kill()