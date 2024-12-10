import pygame
from pytmx import load_pygame, pytmx


class TileMap:
    def __init__(self, tmx_file, scale=2):
        """
        Initialize the TileMap with scaling support and collision handling.
        :param tmx_file: Path to the .tmx file.
        :param scale: Scaling factor for pixelated rendering.
        """
        self.tmx_data = load_pygame(tmx_file)
        self.tile_size = self.tmx_data.tilewidth
        self.scale = scale
        self.scaled_tile_size = self.tile_size * self.scale
        self.width = self.tmx_data.width * self.scaled_tile_size
        self.height = self.tmx_data.height * self.scaled_tile_size

        # Store collision tiles as rectangles
        self.collision_tiles = []
        self.load_collision_layer()

    def load_collision_layer(self):
        """Load collision tiles from the Collision layer."""
        for layer in self.tmx_data.visible_layers:
            if layer.name == "Collision":  # Replace "Collision" with your layer's name
                for x, y, tile in layer.tiles():
                    if tile:  # If a tile exists at this location, it's a collision tile
                        rect = pygame.Rect(
                            x * self.scaled_tile_size,
                            y * self.scaled_tile_size,
                            self.scaled_tile_size,
                            self.scaled_tile_size
                        )
                        self.collision_tiles.append(rect)

    def render(self, screen, camera):
        """Render all the layers of the tilemap with scaling and camera offset."""
        for layer in self.tmx_data.visible_layers:
            if layer.name == "Collision":
                continue
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, tile in layer.tiles():
                    if tile:  # Ensure there's a tile to render
                        # Scale the tile
                        scaled_tile = pygame.transform.scale(
                            tile, (self.scaled_tile_size, self.scaled_tile_size)
                        )

                        # Calculate position with the camera offset
                        dest_x = x * self.scaled_tile_size - camera.camera_rect.left
                        dest_y = y * self.scaled_tile_size - camera.camera_rect.top

                        # Blit the tile if it's within the screen bounds
                        if 0 <= dest_x < camera.screen_width and 0 <= dest_y < camera.screen_height:
                            screen.blit(scaled_tile, (dest_x, dest_y))

    def render_collision_debug(self, screen, camera):
        """Render collision tiles for debugging."""
        for rect in self.collision_tiles:
            # Offset the collision rect by the camera position
            adjusted_rect = rect.move(-camera.camera_rect.left, -camera.camera_rect.top)
            # Draw the collision rect (semi-transparent red)
            pygame.draw.rect(screen, (255, 0, 0, 128), adjusted_rect, 1)

    def render_collision_debug_no_camera(self, screen):
        """Render collision tiles for debugging without camera offset."""
        for rect in self.collision_tiles:
            # Draw the collision rect (semi-transparent red)
            pygame.draw.rect(screen, (0, 255, 0, 128), rect, 1)

    def get_layer_by_name(self, name):
        """Get a specific layer by name."""
        return self.tmx_data.get_layer_by_name(name)



    def get_objects(self, layer_name):
        """Get objects from a specific object layer."""
        return self.tmx_data.get_layer_by_name(layer_name)
