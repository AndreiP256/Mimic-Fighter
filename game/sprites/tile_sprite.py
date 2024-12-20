import pygame


class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, scale, groups):
        super().__init__(groups)
        self.image = pygame.transform.scale(surf, (surf.get_width() * scale, surf.get_height() * scale))
        self.rect = self.image.get_frect(topleft = pos)


class TileSprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, scale, ground = False):
        super().__init__(groups)
        self.image = pygame.transform.scale(surf, (surf.get_width() * scale, surf.get_height() * scale))
        self.rect = self.image.get_frect(topleft = pos)
        if(ground):
            self.ground = True
