import pygame
from config.game_settings import HEALTHDROP_IMAGE_PATH, HEALTHDROP_LIFETIME, HEALTHDROP_AMOUNT

class HealthDrop(pygame.sprite.Sprite):
    def __init__(self, x, y, health_amount):
        super().__init__()
        self.original_image = pygame.image.load(HEALTHDROP_IMAGE_PATH).convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (int(self.original_image.get_width() * 1.5), int(self.original_image.get_height() * 1.5)))  # Scale the image to 1.5 times its original size
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.health_amount = health_amount
        self.spawn_time = pygame.time.get_ticks()  # Record the spawn time

    def update(self, delta_time):
        # Check if the health drop has been active for longer than its lifetime
        if pygame.time.get_ticks() - self.spawn_time > HEALTHDROP_LIFETIME:
            self.kill()

    def apply_to(self, player):
        player.health += self.health_amount
        if player.health > player.max_health:
            player.health = player.max_health
        self.kill()