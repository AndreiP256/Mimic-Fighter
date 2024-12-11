import pygame

from config.game_settings import LOAD_TIME
from game.enemies.enemy import Enemy


class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.surface = pygame.display.get_surface()
        self.offset = pygame.Vector2(0, 0)

    def draw(self, target_offset):
        self.offset.x = -(target_offset[0] - self.surface.get_width() // 2)
        self.offset.y = -(target_offset[1] - self.surface.get_height() // 2)
        for sprite in self.sprites():
            self.surface.blit(sprite.image, sprite.rect.topleft + self.offset)

    def update(self, delta_time):

        for sprite in self.sprites():
            if isinstance(sprite, Enemy) and not sprite.can_update():
                continue
            sprite.update(delta_time)