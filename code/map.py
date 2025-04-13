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
    
    def update_camera(self, player):
        """Update the camera position based on the player's position."""
        self.camera_x = max(0, min(player.x - SCREEN_WIDTH // 2, self.visible_width * SCALED_TILE_SIZE - SCREEN_WIDTH))
        self.camera_y = max(0, min(player.y - SCREEN_HEIGHT // 2, self.visible_height * SCALED_TILE_SIZE - SCREEN_HEIGHT))

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

    def draw(self, screen, offset_x=0, offset_y=0, player=None):
        """Draws the visible part of the map based on the camera position."""
        if player is not None:
            # Center the camera on the player
            self.camera_x = player.x - SCREEN_WIDTH // 2
            self.camera_y = player.y - SCREEN_HEIGHT // 2

            # Ensure the camera doesn't go out of bounds
            self.camera_x = max(0, min(self.camera_x, self.visible_width * SCALED_TILE_SIZE - SCREEN_WIDTH))
            self.camera_y = max(0, min(self.camera_y, self.visible_height * SCALED_TILE_SIZE - SCREEN_HEIGHT))
        else:
            # Use the provided offsets for scrolling
            self.camera_x = offset_x
            self.camera_y = offset_y

        for layer in self.map_layers:
            for y in range(self.visible_height):
                for x in range(self.visible_width):
                    map_x = int(x + self.camera_x // SCALED_TILE_SIZE)  # Convert camera position to tile grid position
                    map_y = int(y + self.camera_y // SCALED_TILE_SIZE)

                    if 0 <= map_y < SCREEN_HEIGHT and 0 <= map_x < SCREEN_WIDTH:
                        tile = layer[y][x]
                        if tile != -1:
                            screen.blit(
                                pygame.transform.scale(self.tiles[tile], (SCALED_TILE_SIZE, SCALED_TILE_SIZE)),
                                (x * SCALED_TILE_SIZE - self.camera_x + map_x, y * SCALED_TILE_SIZE - self.camera_y + map_y)
                            )

    def is_obstacle(self, x, y):
        """Checks if the tile at (x, y) is an obstacle."""
        if x < 0 or y < 0 or y >= len(self.map_layers[0]) or x >= len(self.map_layers[0][0]):
            return True  # Out of bounds = obstacle
        
        for index in OBSTACLE_LAYERS:
            if self.map_layers[index][int(y)][int(x)] != -1:  # If there's a tile, it's an obstacle
                return True
        return False