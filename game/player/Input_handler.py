import pygame

from game.player.player import Player


def move_down(player : Player):
    player.move_down()


def move_up(player : Player):
    player.move_up()


def move_right(player : Player):
    player.move_right()


def move_left(player : Player):
    player.move_left()

def stop_player(player : Player):
    player.stop()

def quit_game(*args, **kwargs):
    pygame.quit()

class InputHandler:
    def __init__(self):
        self.key_down_handlers = {
            pygame.K_DOWN: move_down,
            pygame.K_UP: move_up,
            pygame.K_RIGHT: move_right,
            pygame.K_LEFT: move_left,
            pygame.K_ESCAPE: quit_game
        }

        self.key_up_handlers = {
            pygame.K_DOWN: stop_player,
            pygame.K_UP: stop_player,
            pygame.K_RIGHT: stop_player,
            pygame.K_LEFT: stop_player

        }
        self.mouse_button_down_handlers = {}
        self.mouse_button_up_handlers = {}



    def handle_event(self, event, player : Player):
        if event.type == pygame.KEYDOWN:
            if event.key in self.key_down_handlers:
                self.key_down_handlers[event.key](player)
        elif event.type == pygame.KEYUP:
            if event.key in self.key_up_handlers:
                self.key_up_handlers[event.key](player)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button in self.mouse_button_down_handlers:
                self.mouse_button_down_handlers[event.button](player)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button in self.mouse_button_up_handlers:
                self.mouse_button_up_handlers[event.button](player)
        key = pygame.key.get_pressed()
        if key in self.key_down_handlers:
            self.key_down_handlers[key](player)
    def __call__(self, event, player : Player):
        self.handle_event(event, player)
