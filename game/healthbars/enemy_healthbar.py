import pygame

from config.game_settings import HEALTHBAR_OFFSET_X


class EnemyHealthBar(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, max_hp):
        super().__init__()
        self.w = w
        self.h = h
        self.max_hp = max_hp
        self.curr_hp = max_hp
        self.image = pygame.Surface([w, h])
        self.rect = self.image.get_rect(topleft=(x, y))
        self.update_image()

    def update_details(self, x: int, y: int, curr_hp: int):
        self.curr_hp = curr_hp
        self.rect.topleft = (x + HEALTHBAR_OFFSET_X, y)

    def update(self, delta_time):
        self.update_image()
        if self.curr_hp <= 0:
            super().kill()

    def update_image(self):
        self.image.fill("red")
        fg_width = int(self.w * (self.curr_hp / self.max_hp))
        fg_rect = pygame.Rect(0, 0, fg_width, self.h)
        pygame.draw.rect(self.image, "green", fg_rect)

    def draw(self, surface: pygame.Surface):
        if self.curr_hp > 0:
            surface.blit(self.image, self.rect)