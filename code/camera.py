import pygame
import math
from settings import SCALED_TILE_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH

class Camera:
    def __init__(self, game_map, camera_speed,screen):
        self.map = game_map
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.map_width = self.map.visible_width * SCALED_TILE_SIZE
        self.map_height = self.map.visible_height * SCALED_TILE_SIZE
        self.speed = camera_speed
        self.screen = screen
        self.camera_x = 0
        self.camera_y = 0
        self.camera_target_x = 0
        self.camera_target_y = 0
        self.is_playing = False
   
    def set_camera_position(self, x, y):
        self.is_playing = True
        self.camera_target_x = x
        self.camera_target_y = y
        self.clamp_camera()

    def clamp_camera(self):
        self.camera_x = max(0, min(self.camera_x, self.map_width - SCREEN_WIDTH))
        self.camera_y = max(0, min(self.camera_y, self.map_height - SCREEN_HEIGHT))

    def update_camera(self):
        # Smooth camera movement
        if self.camera_x < self.camera_target_x:
            self.camera_x += min(self.speed, self.camera_target_x - self.camera_x)
        elif self.camera_x > self.camera_target_x:
            self.camera_x -= min(self.speed, self.camera_x - self.camera_target_x)

        if self.camera_y < self.camera_target_y:
            self.camera_y += min(self.speed, self.camera_target_y - self.camera_y)
        elif self.camera_y > self.camera_target_y:
            self.camera_y -= min(self.speed, self.camera_y - self.camera_target_y)

        self.clamp_camera()

    def draw(self,screen):
        self.map.draw(screen, self.camera_x, self.camera_y)

    