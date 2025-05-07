### Refactored map.py
# Fixes tile bounds, optimizes draw loop, and ensures clean camera updates

import pygame
import csv
from settings import TILESET_PATH, TILE_SIZE, SCALED_TILE_SIZE, MAP_CSV_PATHS, OBSTACLE_LAYERS, SCREEN_WIDTH, SCREEN_HEIGHT,TOP_MARGIN

class Map:
    def __init__(self, margin):
        self.tileset = pygame.image.load(TILESET_PATH)
        self.tiles = self._load_tiles()
        self.map_layers = self._load_map_layers(MAP_CSV_PATHS)

        self.visible_width = len(self.map_layers[0][0])
        self.visible_height = len(self.map_layers[0])

        self.camera_x = 0
        self.camera_y = 0
        self.margin = margin

    def update_camera(self, player):
        self.camera_x = max(0, min(player.x - SCREEN_WIDTH // 2, self.visible_width * SCALED_TILE_SIZE - SCREEN_WIDTH))
        self.camera_y = max(0, min(player.y - (SCREEN_HEIGHT - TOP_MARGIN) // 2, self.visible_height * SCALED_TILE_SIZE - SCREEN_HEIGHT))


    def _load_tiles(self):
        tiles = []
        for y in range(0, self.tileset.get_height(), TILE_SIZE):
            for x in range(0, self.tileset.get_width(), TILE_SIZE):
                tile = self.tileset.subsurface(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
                tiles.append(tile)
        return tiles

    def _load_map_layers(self, paths):
        layers = []
        for path in paths:
            with open(path, newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                layers.append([list(map(int, row)) for row in reader])
        return layers

    def draw(self, screen, offset_x=0, offset_y=0, player=None):
        if player:
            self.update_camera(player)
        else:
            self.camera_x = offset_x
            self.camera_y = offset_y

        start_col = int(self.camera_x // SCALED_TILE_SIZE)
        end_col = int((self.camera_x + SCREEN_WIDTH) // SCALED_TILE_SIZE) + 1
        start_row = int(self.camera_y // SCALED_TILE_SIZE)
        end_row = int((self.camera_y + SCREEN_HEIGHT) // SCALED_TILE_SIZE) + 1

        if self.margin:
            for layer in self.map_layers:
                for y in range(start_row, min(end_row, len(layer))):
                    for x in range(start_col, min(end_col, len(layer[0]))):
                        tile_index = layer[y][x]
                        if tile_index != -1:
                            screen.blit(
                                pygame.transform.scale(self.tiles[tile_index], (SCALED_TILE_SIZE, SCALED_TILE_SIZE)),
                                (x * SCALED_TILE_SIZE - self.camera_x, y * SCALED_TILE_SIZE - self.camera_y + TOP_MARGIN)
                            )
        else: 
            for layer in self.map_layers:
                for y in range(start_row, min(end_row, len(layer))):
                    for x in range(start_col, min(end_col, len(layer[0]))):
                        tile_index = layer[y][x]
                        if tile_index != -1:
                            screen.blit(
                                pygame.transform.scale(self.tiles[tile_index], (SCALED_TILE_SIZE, SCALED_TILE_SIZE)),
                                (x * SCALED_TILE_SIZE - self.camera_x, y * SCALED_TILE_SIZE - self.camera_y)
                            )


    def is_obstacle(self, x, y):
        if x < 0 or y < 0 or y >= len(self.map_layers[0]) or x >= len(self.map_layers[0][0]):
            return True
        for index in OBSTACLE_LAYERS:
            if self.map_layers[index][int(y)][int(x)] != -1:
                return True
        return False
