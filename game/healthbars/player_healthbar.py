import pygame

from game.healthbars.healthbar import HealthBar

class PlayerHealthBar(HealthBar):
    def __init__(self, x, y, w, h, max_hp):
        super().__init__(x, y, w, h, max_hp)
        self.x = x
        self.y = y
        self.font = pygame.font.Font(None, 24)
        self.border_color = (255, 255, 255)  # White border color
        self.bg_color = (50, 50, 50, 128)  # Dark gray background color with alpha
        self.fg_color = (255, 0, 0, 128)  # Green foreground color with alpha

    def update(self, x: int, y: int, curr_hp: int):
        super().update(x, y, curr_hp)

    def draw(self, surface):
        # Create a translucent surface for the health bar
        health_bar_surface = pygame.Surface((self.w, self.h), pygame.SRCALPHA)

        # Draw the border
        border_rect = pygame.Rect(0, 0, self.w, self.h)
        pygame.draw.rect(health_bar_surface, self.border_color, border_rect, 2)

        # Draw the background
        bg_rect = pygame.Rect(2, 2, self.w - 4, self.h - 4)
        pygame.draw.rect(health_bar_surface, self.bg_color, bg_rect)

        # Draw the foreground (health bar)
        fg_rect = pygame.Rect(2, 2, int((self.w - 4) * (self.curr_hp / self.max_hp)), self.h - 4)
        pygame.draw.rect(health_bar_surface, self.fg_color, fg_rect)

        # Render the current HP text
        hp_text = self.font.render(f'{self.curr_hp}/{self.max_hp}', True, (255, 255, 255))
        # Center the text on the health bar
        text_rect = hp_text.get_rect(center=(self.w // 2, self.h // 2))
        health_bar_surface.blit(hp_text, text_rect)

        # Blit the health bar surface onto the main surface
        surface.blit(health_bar_surface, (self.x, self.y))