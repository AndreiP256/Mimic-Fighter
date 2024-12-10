import pygame.draw

from config.game_settings import HEALTHBAR_OFFSET_X, HEALTHBAR_OFFSET_Y


class HealthBar:
    def __init__(self, x, y, w, h, max_hp):
        self.w = w
        self.h = h
        self.max_hp = max_hp
        self.curr_hp = max_hp
        self.bg_rect = pygame.Rect(x, y, w, h)
        self.fg_rect = pygame.Rect(x, y, w, h)

    def update(self, x : int, y : int, curr_hp : int):
        self.curr_hp = curr_hp
        self.bg_rect.topleft = (x + HEALTHBAR_OFFSET_X, y + HEALTHBAR_OFFSET_Y)
        self.fg_rect.topleft = (x + HEALTHBAR_OFFSET_X, y + HEALTHBAR_OFFSET_Y)
        self.fg_rect.width = int(self.bg_rect.width * (self.curr_hp / self.max_hp))

    def draw(self, surface : pygame.Surface):
        if self.curr_hp > 0:
            pygame.draw.rect(surface, "red", self.bg_rect)
            pygame.draw.rect(surface, "green", self.fg_rect)
