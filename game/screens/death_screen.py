import pygame
import pygame.gfxdraw

from config.game_settings import DEATH_IMAGE_WIDTH, IMAGE_SCALE, DEATH_IMAGE_HEIGHT, BUTTON_SCALE
from game.screens.button import Button


def init_button(path, x, y):
    return Button(x, y, BUTTON_SCALE, path)


def blur_surface(surface, amount):
    scale = 1.0 / amount
    surf_size = surface.get_size()
    scale_size = (int(surf_size[0] * scale), int(surf_size[1] * scale))
    surf = pygame.transform.smoothscale(surface, scale_size)
    surf = pygame.transform.smoothscale(surf, surf_size)
    return surf


def load_bg_image(bg_image_path):
    if bg_image_path:
        return pygame.image.load(bg_image_path).convert_alpha()


class DeathScreen:
    def __init__(self, screen, restart_path, exit_path, text_image_path, menu_path=None, bg_image_path=None):
        self.screen = screen
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()

        button_width = self.width // 3  # Assuming each button takes up 1/4 of the screen width
        button_height = 50  # Assuming a fixed height for buttons
        button_y = self.height - 200 - button_height // 2

        self.restart_button = init_button(restart_path, self.width // 4 - button_width // 2, button_y)
        self.exit_button = init_button(exit_path, 3 * self.width // 4 - button_width // 2, button_y)

        self.buttons = [self.restart_button, self.exit_button]

        self.text_image = pygame.image.load(text_image_path).convert_alpha()
        self.text_image = pygame.transform.scale(self.text_image,
                                                (int(DEATH_IMAGE_WIDTH * IMAGE_SCALE), int(DEATH_IMAGE_HEIGHT *
                                                                                            IMAGE_SCALE)))
        self.bg_image = load_bg_image(bg_image_path)
        self.bg_image = pygame.transform.scale(self.bg_image, (self.width, self.height)) if self.bg_image else None

    def draw(self):
        translucent_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.screen.blit(translucent_surface, (0, 0))
        self.draw_image(self.text_image, self.screen.get_width() // 2, self.screen.get_height() // 2)
        for button in self.buttons:
            if button.draw(self.screen):
                return button

        pygame.display.update()

    def draw_image(self, image, x, y):
        image_rect = image.get_rect(center=(x, y))
        self.screen.blit(image, image_rect)

    def do_death_loop(self) -> str:
        for _ in range(15):
            blurred_screen = blur_surface(self.screen.copy(), 10)
            self.screen.blit(blurred_screen, (0, 0))
            pygame.display.update()

        # Fade-out effect to background image
        if self.bg_image:
            for alpha in range(0, 256, 5):
                self.bg_image.set_alpha(alpha)
                self.screen.blit(self.bg_image, (0, 0))
                pygame.display.update()
                pygame.time.delay(5)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
            button = self.draw()
            if button is None:
                continue
            elif button == self.restart_button:
                return "restart"
            elif button == self.exit_button:
                return "exit"