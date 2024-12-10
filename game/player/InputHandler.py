import pygame
from game.sprites.colision_handler import ColisionHandler

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

def sprint(player : Player):
    player.sprint()

def stop_sprint(player: Player):
    player.stop_sprint()

def player_chop(player: Player, coliHandler: ColisionHandler):
    player.do_chop()
    coliHandler.chop_attack(player)

def stop_chop(player: Player):
    player.stop_attack()

def player_slash(player: Player, coliHandler: ColisionHandler):
    player.do_slash()
    coliHandler.slash_attack(player)


def player_roll(player: Player):
    player.roll()

class InputHandler:
    def __init__(self, coliHandler: ColisionHandler):
        self.key_down_handlers = {
            pygame.K_DOWN: move_down,
            pygame.K_UP: move_up,
            pygame.K_RIGHT: move_right,
            pygame.K_LEFT: move_left,
            pygame.K_w: move_up,
            pygame.K_s: move_down,
            pygame.K_a: move_left,
            pygame.K_d: move_right,
            pygame.K_ESCAPE: quit_game,
            pygame.K_LSHIFT  : sprint,
            pygame.K_SPACE: player_roll
        }
        self.movement_handlers = [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_UP, pygame.K_DOWN,
                                  pygame.K_RIGHT, pygame.K_LEFT]
        self.key_up_handlers = {
            pygame.K_DOWN: stop_player,
            pygame.K_UP: stop_player,
            pygame.K_RIGHT: stop_player,
            pygame.K_LEFT: stop_player,
            pygame.K_w: stop_player,
            pygame.K_s: stop_player,
            pygame.K_a: stop_player,
            pygame.K_d: stop_player,
            pygame.K_LSHIFT : stop_sprint,
        }
        self.coliHandler = coliHandler
        self.mouse_button_down_handlers = {
            3: player_chop,
            1: player_slash
        }
        self.attack_handlers = {
            1: player_slash,
            3: player_chop,
            pygame.K_l: player_slash,
            pygame.K_k: player_chop
        }
        # self.mouse_button_up_handlers = {
        #     1: stop_chop
        #     # 2: stop_slash
        # }



    def handle_event(self, event, player : Player):
        if event.type == pygame.KEYDOWN:
            if event.key in self.key_down_handlers:
                self.key_down_handlers[event.key](player)
            elif event.key in self.attack_handlers:
                self.attack_handlers[event.key](player, self.coliHandler)
        elif event.type == pygame.KEYUP:
            if event.key in self.key_up_handlers:
                self.key_up_handlers[event.key](player)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button in self.attack_handlers:
                self.mouse_button_down_handlers[event.button](player, self.coliHandler)
        # elif event.type == pygame.MOUSEBUTTONUP:
        #     if event.button in self.mouse_button_up_handlers:
        #         self.mouse_button_up_handlers[event.button](player)

    def __call__(self, event, player : Player):
        self.handle_event(event, player)

    def handle_key(self, player : Player, keys):
        for key in self.movement_handlers:
            if keys[key]:
                self.key_down_handlers[key](player)