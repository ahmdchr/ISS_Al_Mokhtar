import pygame
import csv
from settings import TILESET_PATH, TILE_SIZE, SCALED_TILE_SIZE, MAP_CSV_PATHS, OBSTACLE_LAYERS, SCREEN_WIDTH, SCREEN_HEIGHT

class Map:
    """Handles loading, rendering, and managing the game map."""
    def __init__(self):
        self.tileset = pygame.image.load(TILESET_PATH)
        self.tiles = self.load_tiles()
        self.map_layers = self.load_map_layers(MAP_CSV_PATHS)

        # Get the map's width and height in tiles
        self.visible_width = len(self.map_layers[0][0])  
        self.visible_height = len(self.map_layers[0])  
        
        # Camera position
        self.camera_x = 0
        self.camera_y = 0

    def load_tiles(self):
        """Extracts individual tiles from the tileset image."""
        tiles = []
        for y in range(0, self.tileset.get_height(), TILE_SIZE):
            for x in range(0, self.tileset.get_width(), TILE_SIZE):
                tile = self.tileset.subsurface(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
                tiles.append(tile)
        return tiles

    def load_map_layers(self, paths):
        """Loads map data from CSV files into layers."""
        layers = []
        for path in paths:  
            with open(path, newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                layers.append([list(map(int, row)) for row in reader])
        return layers
    
    def update_camera(self, player_x, player_y):
        """Centers the camera on the player while keeping it within map boundaries."""
        half_screen_x = SCREEN_WIDTH // 2
        half_screen_y = SCREEN_HEIGHT // 2

        # Convert player position to tile coordinates
        tile_x = int(player_x // SCALED_TILE_SIZE)
        tile_y = int(player_y // SCALED_TILE_SIZE)

        # Update camera position
        self.camera_x = max(0, min(tile_x - self.visible_width // 2, len(self.map_layers[0][0]) - self.visible_width))
        self.camera_y = max(0, min(tile_y - self.visible_height // 2, len(self.map_layers[0]) - self.visible_height))

    def draw(self, screen, x_offset=0, y_offset=0):
        """Draws the visible part of the map based on the camera position."""
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
        """Checks if the tile at (x, y) is an obstacle."""
        if x < 0 or y < 0 or y >= len(self.map_layers[0]) or x >= len(self.map_layers[0][0]):
            return True  # Out of bounds = obstacle
        
        for index in OBSTACLE_LAYERS:
            if self.map_layers[index][int(y)][int(x)] != -1:  # If there's a tile, it's an obstacle
                return True
        return False

    def move_camera(self, dx, dy):
        """Moves the camera within the allowed map boundaries, avoiding obstacles."""
        new_x = self.camera_x + dx
        new_y = self.camera_y + dy
        
        if not self.is_obstacle(new_x, new_y):
            self.camera_x = max(0, min(new_x, len(self.map_layers[0][0]) - self.visible_width))
            self.camera_y = max(0, min(new_y, len(self.map_layers[0]) - self.visible_height))
