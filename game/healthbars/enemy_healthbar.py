import pygame.draw

from config.game_settings import HEALTHBAR_OFFSET_X, HEALTHBAR_OFFSET_Y
from game.healthbars.healthbar import HealthBar


class EnemyHealthBar(HealthBar):
    def __init__(self, x, y, w, h, max_hp):
        super().__init__(x, y, w, h, max_hp)

    def update(self, x : int, y : int, curr_hp : int):
        super().update(x, y, curr_hp)
        self.bg_rect.topleft = (x + HEALTHBAR_OFFSET_X, y + HEALTHBAR_OFFSET_Y)
        self.fg_rect.topleft = (x + HEALTHBAR_OFFSET_X, y + HEALTHBAR_OFFSET_Y)
