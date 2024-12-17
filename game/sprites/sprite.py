import pygame

class Spritesheet():
    def __init__(self, filename):
        self.spritesheet = pygame.image.load(filename).convert_alpha()

    def get_image(self, x, y, width, height, scale = 1):
        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        if scale:
            image = pygame.transform.scale(image, (width * scale, height * scale))
        return image