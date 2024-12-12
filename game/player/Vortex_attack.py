import pygame

class AnimatedVortex(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, scale: float, image_path: str, groups):
        super().__init__(groups)
        self.frames = [pygame.image.load(f"{image_path}{i:04d}.png").convert_alpha() for i in range(0, 82)]
        self.frames = [pygame.transform.scale(frame, (int(frame.get_width() * scale),
                                              int(frame.get_height() * scale))) for frame in self.frames]
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_frect()
        self.rect.center = (x, y)
        self.animation_time = 100  # Time in milliseconds between frames
        self.last_update = pygame.time.get_ticks()
        self.finished_animation = False
        print("Vortex created")
        print(groups)
        print(self in groups)

    def update(self, delta_time):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_time:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]

        # # Check if the health drop has been active for longer than its lifetime
        # if self.current_frame == 81:
        #     super().kill()
