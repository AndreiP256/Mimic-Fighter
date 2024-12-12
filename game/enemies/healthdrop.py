import pygame
from game.sounds.sound_manager import SoundManager
from config.game_settings import HEALTHDROP_IMAGE_PATH, HEALTHDROP_LIFETIME, HEALTHDROP_AMOUNT, HEALTHDROP_SCALE

class HealthDrop(pygame.sprite.Sprite):
    def __init__(self, x, y, health_amount, groups):
        super().__init__(groups)
        self.frames = [pygame.image.load(f"{HEALTHDROP_IMAGE_PATH}_{i}.png").convert_alpha() for i in range(1, 5)]
        self.frames = [pygame.transform.scale(frame, (int(frame.get_width() * HEALTHDROP_SCALE),
                                                      int(frame.get_height() * HEALTHDROP_SCALE))) for frame in self.frames]
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.sound_manager = SoundManager()
        self.health_amount = health_amount
        self.spawn_time = pygame.time.get_ticks()
        self.animation_time = 100  # Time in milliseconds between frames
        self.last_update = pygame.time.get_ticks()

    def update(self, delta_time):
        # Update animation
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_time:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]

        # Check if the health drop has been active for longer than its lifetime
        if now - self.spawn_time > HEALTHDROP_LIFETIME:
            super().kill()

    def apply_to(self, player):
        player.health += self.health_amount
        self.sound_manager.play_sound("healthdrop")
        if player.health > player.max_health:
            player.health = player.max_health
        self.kill()