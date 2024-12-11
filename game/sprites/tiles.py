import pygame
from pytmx import load_pygame, pytmx

from config.game_settings import TILE_SCALE, TILE_SIZE, DECOR_SCALE
from game.sprites.tile_sprite import TileSprite, CollisionSprite


class TileMap:
    def __init__(self, tmx_file, sprite_group=None, collison_group = None, screen=None):
        self.tmx_data = load_pygame(tmx_file)
        self.scaled_tile_size = TILE_SIZE * TILE_SCALE
        self.width = self.tmx_data.width * self.scaled_tile_size
        self.height = self.tmx_data.height * self.scaled_tile_size
        self.group = sprite_group
        self.collision_group = collison_group
        self.load_collision_layer()

    def load_collision_layer(self):
        for layer in self.tmx_data.visible_layers:
            if layer.name == "Collision":
                for x, y, tile in layer.tiles():
                    if tile:
                        CollisionSprite((x * TILE_SIZE * TILE_SCALE, y * TILE_SIZE * TILE_SCALE),
                                        tile, TILE_SCALE, self.collision_group)

    def render_collision_debug(self, screen):
        for rect in self.collision_tiles:
            pygame.draw.rect(screen, (255, 0, 0, 128), rect, 1)

    def get_layer_by_name(self, name):
        return self.tmx_data.get_layer_by_name(name)

    def setup(self):
        for x, y, image in self.tmx_data.get_layer_by_name('Tile Layer 1').tiles():
            TileSprite((x * TILE_SIZE * TILE_SCALE, y * TILE_SIZE * TILE_SCALE), image, self.group, TILE_SCALE)
        for x, y, image in self.tmx_data.get_layer_by_name('Decor').tiles():
            TileSprite((x * TILE_SIZE * TILE_SCALE, y * TILE_SIZE * TILE_SCALE), image, self.group, TILE_SCALE)
        self.load_collision_layer()

    def reset(self):
        for tile in self.group:
            tile.kill()
        for tile in self.collision_group:
            tile.kill()