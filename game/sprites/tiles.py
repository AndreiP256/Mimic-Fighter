import pygame
from pytmx import load_pygame, pytmx

class TileMap:
    def __init__(self, tmx_file, scale=2):
        self.tmx_data = load_pygame(tmx_file)
        self.tile_size = self.tmx_data.tilewidth
        self.scale = scale
        self.scaled_tile_size = self.tile_size * self.scale
        self.width = self.tmx_data.width * self.scaled_tile_size
        self.height = self.tmx_data.height * self.scaled_tile_size

        self.collision_tiles = []
        self.load_collision_layer()

    def load_collision_layer(self):
        for layer in self.tmx_data.visible_layers:
            if layer.name == "Collision":
                for x, y, tile in layer.tiles():
                    if tile:
                        rect = pygame.Rect(
                            x * self.scaled_tile_size,
                            y * self.scaled_tile_size,
                            self.scaled_tile_size,
                            self.scaled_tile_size
                        )
                        self.collision_tiles.append(rect)

    def render(self, screen):
        for layer in self.tmx_data.visible_layers:
            if layer.name == "Collision":
                continue
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, tile in layer.tiles():
                    if tile:
                        scaled_tile = pygame.transform.scale(
                            tile, (self.scaled_tile_size, self.scaled_tile_size)
                        )
                        dest_x = x * self.scaled_tile_size
                        dest_y = y * self.scaled_tile_size
                        screen.blit(scaled_tile, (dest_x, dest_y))

    def render_collision_debug(self, screen):
        for rect in self.collision_tiles:
            pygame.draw.rect(screen, (255, 0, 0, 128), rect, 1)

    def render_collision_debug_no_camera(self, screen):
        for rect in self.collision_tiles:
            pygame.draw.rect(screen, (0, 255, 0, 128), rect, 1)

    def get_layer_by_name(self, name):
        return self.tmx_data.get_layer_by_name(name)

    def get_objects(self, layer_name):
        return self.tmx_data.get_layer_by_name(layer_name)