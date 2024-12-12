import pygame

from config.game_settings import VORTEX_PATH, VORTEX_SCALE


class AnimatedVortex(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, groups):
        super().__init__(groups)
        self.frames = [pygame.image.load(f"{VORTEX_PATH}{i:04d}.png").convert_alpha() for i in range(0, 82)]
        self.frames = [pygame.transform.scale(frame, (int(frame.get_width() * VORTEX_SCALE),
                                              int(frame.get_height() * VORTEX_SCALE))) for frame in self.frames]
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_frect()
        self.rect.center = (x, y)
        self.animation_time = 5  # Time in milliseconds between frames
        self.last_update = pygame.time.get_ticks()
        self.finished_animation = False

    def update(self, delta_time):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_time:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]

        # # Check if the health drop has been active for longer than its lifetime
        if self.current_frame == 81:
            super().kill()

    def is_done(self):
        return self.current_frame > 15
