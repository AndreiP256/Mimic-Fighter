# game/player.py
import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (100, 100)

    def update(self, delta_time):
        self.rect.center = pygame.mouse.get_pos()

    def get_position(self):
        return self.rect.center

    def take_damage(self, damage):
        pass