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


        ground_sprites = [sprite for sprite in self if hasattr(sprite, "ground")]
        object_sprites = [sprite for sprite in self if not hasattr(sprite, "ground")]
        print("Ground Sprites: ", ground_sprites)
        print("Object Sprites: ", object_sprites)
        for layer in [ground_sprites, object_sprites]:
            for sprite in sorted(layer, key = lambda sprite: sprite.rect.centery):
                self.surface.blit(sprite.image, sprite.rect.topleft + self.offset)


    def update(self, delta_time):
        for sprite in self.sprites():
            if isinstance(sprite, Enemy) and not sprite.can_update():
                continue
            sprite.update(delta_time)
