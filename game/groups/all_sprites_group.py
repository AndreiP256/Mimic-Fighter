import pygame


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