import pygame
import csv
from settings import TILESET_PATH, TILE_SIZE, SCALED_TILE_SIZE, MAP_CSV_PATHS, OBSTACLE_LAYERS, SCREEN_WIDTH, SCREEN_HEIGHT

class Map:
    def __init__(self):
        self.tileset = pygame.image.load(TILESET_PATH)
        self.tiles = self.load_tiles()
        self.map_layers = self.load_map_layers(MAP_CSV_PATHS)
        
        self.visible_width = len(self.map_layers[0][0])  
        self.visible_height = len(self.map_layers[0])  
        
        self.camera_x = 0
        self.camera_y = 0

    def load_tiles(self):
        tiles = []
        for y in range(0, self.tileset.get_height(), TILE_SIZE):
            for x in range(0, self.tileset.get_width(), TILE_SIZE):
                tile = self.tileset.subsurface(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
                tiles.append(tile)
        return tiles

    def load_map_layers(self, paths):
        layers = []
        for path in paths:  
            with open(path, newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                layers.append([list(map(int, row)) for row in reader])
        return layers

    def draw(self, screen, x_offset=0, y_offset=0):
        """Draw the map at an adjustable position."""
        for layer in self.map_layers:
            for y in range(self.visible_height):
                for x in range(self.visible_width):
                    map_x = x + self.camera_x
                    map_y = y + self.camera_y
                    
                    if 0 <= map_y < len(layer) and 0 <= map_x < len(layer[0]):
                        tile = layer[map_y][map_x]
                        if tile != -1:
                            screen.blit(
                                pygame.transform.scale(self.tiles[tile], (SCALED_TILE_SIZE, SCALED_TILE_SIZE)),
                                (x * SCALED_TILE_SIZE + x_offset, y * SCALED_TILE_SIZE + y_offset)
                            )


    def is_obstacle(self, x, y):
        #Check if the tile at (x, y) is an obstacle.
        if x < 0 or y < 0 or y >= len(self.map_layers[0]) or x >= len(self.map_layers[0][0]):
            return True  # Out of bounds = obstacle
        
        for index in OBSTACLE_LAYERS:
            if self.map_layers[index][int(y)][int(x)] != -1:  # If there's a tile, it's an obstacle
                return True
        return False

    def move_camera(self, dx, dy):
        new_x = self.camera_x + dx
        new_y = self.camera_y + dy
        
        if not self.is_obstacle(new_x, new_y):
            self.camera_x = max(0, min(new_x, len(self.map_layers[0][0]) - self.visible_width))
            self.camera_y = max(0, min(new_y, len(self.map_layers[0]) - self.visible_height))
