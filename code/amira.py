import pygame
from settings import PLAYER_SPEED, ANIMATION_SPEED

class Character:
    def __init__(self, game_map):
        self.x, self.y = 600, 300  # Initial player position
        self.direction = 0  # 0: down, 1: left, 2: right, 3: up
        self.current_frame = 0  # Frame for animation
        self.animation_timer = 0  # Timer to control animation speed
        self.speed = PLAYER_SPEED  # Movement speed
        self.animation_speed = ANIMATION_SPEED  # Animation speed setting
        self.map = game_map # Reference to the game map
        self.facing = "down"

        # Load animations for different states
        self.image_idle = self.load_all_images('idle_animation_amira', 3)
        self.image_run = self.load_all_images('run_animation_amira', 4)


    def load_all_images(self, action, frames, size=(64, 64)):
        """Load animation frames for different directions."""
        return {
            'down': [pygame.transform.scale(pygame.image.load(f'{action}/amira_down/amira_down_{i+1}.png'), size) for i in range(frames)],
            'right': [pygame.transform.scale(pygame.image.load(f'{action}/amira_right/amira_right_{i+1}.png'), size) for i in range(frames)],
            'left': [pygame.transform.scale(pygame.image.load(f'{action}/amira_left/amira_left_{i+1}.png'), size) for i in range(frames)],
            'up': [pygame.transform.scale(pygame.image.load(f'{action}/amira_up/amira_up_{i+1}.png'), size) for i in range(frames)]
        }

    def draw(self, screen):
        """Draw the correct animation frame based on player state."""
        directions = ['down', 'left', 'right', 'up']
        direction = directions[self.direction]
        screen.blit(self.image_idle[direction][self.current_frame % 3], (self.x, self.y))
