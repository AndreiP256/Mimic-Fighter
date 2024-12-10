import pygame

from game.healthbars.healthbar import HealthBar


class PlayerHealthBar(HealthBar):
    def __init__(self, x, y, w, h, max_hp):
        super().__init__(x, y, w, h, max_hp)
        self.x = x
        self.y = y
        self.font = pygame.font.Font(None, 24)

    def update(self, x: int, y: int, curr_hp: int):
        super().update(x, y, curr_hp)

    def draw(self, surface):
        super().draw(surface)
        hp_text = self.font.render(f'{self.curr_hp}/{self.max_hp}', True, (255, 255, 255))
        text_rect = hp_text.get_rect(center=(self.x + self.w // 2, self.y + self.h // 2))
        surface.blit(hp_text, text_rect)