import pygame
import pygame.gfxdraw

from config.game_settings import BUTTON_SCALE
from screens.button import Button


def init_button(path, x, y):
    return Button(x, y, 5, path)


def blur_surface(surface, amount):
    """Applies a Gaussian blur to the given surface."""
    scale = 1.0 / amount
    surf_size = surface.get_size()
    scale_size = (int(surf_size[0] * scale), int(surf_size[1] * scale))
    surf = pygame.transform.smoothscale(surface, scale_size)
    surf = pygame.transform.smoothscale(surf, surf_size)
    return surf


class PauseScreen:
    def __init__(self, screen, resume_path, restart_path, exit_path):
        self.screen = screen
        self.width = self.screen.get_width() // 2
        self.height = self.screen.get_height() // 2
        self.x = self.screen.get_width() // 4
        self.y = self.screen.get_height() // 4
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        button_width = self.width // 2 - 50
        button_height = 50  # Assuming a fixed height for buttons
        button_x = self.x + (self.width - button_width) // 2

        self.resume_button = init_button(resume_path, button_x, self.y + 50)
        self.restart_button = init_button(restart_path, button_x, self.y + 150)
        self.exit_button = init_button(exit_path, button_x, self.y + 250)

        self.buttons = [self.resume_button, self.restart_button, self.exit_button]

    def draw(self):

        translucent_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # Draw the translucent surface
        self.screen.blit(translucent_surface, (self.x, self.y))

        # Draw buttons
        for button in self.buttons:
            if button.draw(self.screen):
                return button

        pygame.display.update()

    def do_pause_loop(self) -> str:
        for _ in range(15):
            blurred_screen = blur_surface(self.screen.copy(), 10)
            self.screen.blit(blurred_screen, (0, 0))
            pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
            button = self.draw()
            if button is None:
                continue
            elif button == self.resume_button:
                return "resume"
            elif button == self.restart_button:
                return "restart"
            elif button == self.exit_button:
                return "exit"