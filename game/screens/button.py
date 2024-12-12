import pygame

class Button:
    def __init__(self, x: int, y: int, scale: float, image_path: str):
        self.frames = [pygame.image.load(f"{image_path}{i}.png").convert_alpha() for i in range(1, 5)]
        self.frames = [pygame.transform.scale(frame, (int(frame.get_width() * scale),
                                                      int(frame.get_height() * scale))) for frame in self.frames]
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.animation_time = 100  # Time in milliseconds between frames
        self.last_update = pygame.time.get_ticks()
        self.finished_animation = False

    def play_animation(self, surface):
        while not self.finished_animation:
            now = pygame.time.get_ticks()
            if now - self.last_update > self.animation_time:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                if self.current_frame == 0:
                    self.finished_animation = True
                self.image = self.frames[self.current_frame]
            surface.blit(self.image, (self.rect.x, self.rect.y))
            pygame.display.update()

    def draw(self, surface) -> bool:
        action = False
        self.finished_animation = False
        pos = pygame.mouse.get_pos()

        # Check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            self.image = self.brighten_image(self.frames[self.current_frame])
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.play_animation(surface)
                self.clicked = True
                action = True
        else:
            self.image = self.frames[self.current_frame]

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # Draw button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action

    def brighten_image(self, image):
        """Brighten the image by increasing its RGB values."""
        bright_image = image.copy()
        bright_array = pygame.surfarray.pixels3d(bright_image)
        bright_array[:, :, :] = bright_array[:, :, :] + 50  # Increase brightness
        bright_array[bright_array > 255] = 255  # Cap values at 255
        return bright_image