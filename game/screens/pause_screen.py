import pygame
from PIL.ImageChops import screen

from game.button import Button


def init_button(path, x, y):
    image = pygame.image.load(path).convert_alpha()
    return Button(x, y, image, 5)


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
        pygame.draw.rect(self.screen, "lightblue", self.rect)
        for button in self.buttons:
            if button.draw(self.screen):
                return button
        pygame.display.update()

    def do_pause_loop(self) -> str:
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