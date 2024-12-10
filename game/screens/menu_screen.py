import pygame
from game.screens.button import Button

def init_button(path, x, y):
    image = pygame.image.load(path).convert_alpha()
    return Button(x, y, image, 5)

class MainMenuScreen:
    def __init__(self, screen, start_path, exit_path, bg_image=None, bg_color="darkgreen"):
        self.screen = screen
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.bg_color = bg_color
        self.rect = pygame.Rect(0, 0, self.width, self.height)

        button_width = self.width // 4  # Assuming each button takes up 1/4 of the screen width
        button_height = 50  # Assuming a fixed height for buttons
        button_y = self.height - 200 - button_height // 2

        self.start_button = init_button(start_path, self.width // 4 - button_width // 2, button_y)
        self.exit_button = init_button(exit_path, 3 * self.width // 4 - button_width // 2, button_y)

        self.buttons = [self.start_button, self.exit_button]

    def draw(self):
        pygame.draw.rect(self.screen, self.bg_color, self.rect)
        for button in self.buttons:
            if button.draw(self.screen):
                return button
        pygame.display.update()

    def do_menu_loop(self) -> str:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
            button = self.draw()
            if button is None:
                continue
            elif button == self.start_button:
                return "start"
            elif button == self.exit_button:
                return "exit"