from pytmx import load_pygame

from config.game_settings import TILE_SCALE, TILE_SIZE
from sprites.tile_sprite import TileSprite, CollisionSprite


class TileMap:
    def __init__(self, tmx_file, sprite_group=None, collison_group = None, screen=None):
        self.tmx_data = load_pygame(tmx_file)
        self.scaled_tile_size = TILE_SIZE * TILE_SCALE
        self.width = self.tmx_data.width * self.scaled_tile_size
        self.height = self.tmx_data.height * self.scaled_tile_size
        self.group = sprite_group
        self.collision_group = collison_group
        self.enemy_tiles = []
        self.boss_tile = None
        self.player_spawn : tuple = (None, None)

    def setup(self):
        offset = TILE_SCALE * TILE_SIZE
        for x, y, image in self.tmx_data.get_layer_by_name('Ground').tiles():
            TileSprite((x * offset, y * offset), image, self.group, TILE_SCALE, ground=True)
        for x, y, image in self.tmx_data.get_layer_by_name('Decor').tiles():
            TileSprite((x * offset, y * offset), image, self.group, TILE_SCALE)
        for x, y, image in self.tmx_data.get_layer_by_name('Collision').tiles():
            CollisionSprite((x * offset, y * offset), image, TILE_SCALE, self.collision_group)
        for obj in self.tmx_data.get_layer_by_name('Enemies'):
            if obj.name != 'Spawn':
                if obj.name == 'Boss':
                    self.boss_tile = (obj.x * TILE_SCALE, obj.y * TILE_SCALE)
                else:
                    self.enemy_tiles.append((obj.x * TILE_SCALE, obj.y * TILE_SCALE))
        obj = self.tmx_data.get_object_by_name('Spawn')
        self.player_spawn = (obj.x * TILE_SCALE, obj.y * TILE_SCALE)

    def reset(self):
        for tile in self.group:
            tile.kill()
        for tile in self.collision_group:
            tile.kill()