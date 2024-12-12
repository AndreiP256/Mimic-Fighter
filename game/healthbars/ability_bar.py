import pygame

from game.healthbars.healthbar import HealthBar
from config.game_settings import ABILITY_CONTOUR_IMAGE_PATH, ABILITY_IMAGE_PATH, HEALTHBAR_SCALE_FACTOR

class AbilityBar(HealthBar):
    def __init__(self, x, y, w, h, max_hp):
        super().__init__(x, y, w, h, max_hp)
        self.x = x
        self.y = y
        self.font = pygame.font.Font(None, 24)

        # Load images
        self.contour_image = pygame.image.load(ABILITY_CONTOUR_IMAGE_PATH).convert_alpha()
        self.healthbar_image = pygame.image.load(ABILITY_IMAGE_PATH).convert_alpha()

        # Scale images
        self.contour_image = pygame.transform.scale(self.contour_image,
            (int(self.contour_image.get_width() * HEALTHBAR_SCALE_FACTOR), int(self.contour_image.get_height() * HEALTHBAR_SCALE_FACTOR)))
        self.healthbar_image = pygame.transform.scale(self.healthbar_image,
            (int(self.healthbar_image.get_width() * HEALTHBAR_SCALE_FACTOR), int(self.healthbar_image.get_height() * HEALTHBAR_SCALE_FACTOR)))

        # Get the dimensions of the health bar image
        self.healthbar_width = self.healthbar_image.get_width()
        self.healthbar_height = self.healthbar_image.get_height()

        # Create a surface for the health bar
        self.healthbar_surface = pygame.Surface((self.healthbar_width, self.healthbar_height), pygame.SRCALPHA)

    def update_details(self, curr_hp: int):
        super().update(0, 0, curr_hp)
        self.curr_hp = curr_hp
        # Calculate the width of the health bar based on the current health
        healthbar_current_width = int(self.healthbar_width * (self.curr_hp / self.max_hp))
        # Clear the health bar surface
        self.healthbar_surface.fill((0, 0, 0, 0))
        # Blit the health bar image onto the surface with the updated width
        self.healthbar_surface.blit(self.healthbar_image, (0, 0), (0, 0, healthbar_current_width, self.healthbar_height))

    def draw(self, surface):
        # Blit the health bar surface
        surface.blit(self.healthbar_surface, (self.x, self.y))
        # Blit the contour image
        surface.blit(self.contour_image, (self.x, self.y))