import pygame
from settings import PLAYER_SPEED, ANIMATION_SPEED, SCALED_TILE_SIZE

class Player:
    def __init__(self, game_map):
        self.x, self.y = 300, 300  # Initial player position
        self.direction = 0  # 0: down, 1: left, 2: right, 3: up
        self.current_frame = 0  # Frame for animation
        self.animation_timer = 0  # Timer to control animation speed
        self.speed = PLAYER_SPEED  # Movement speed
        self.animation_speed = ANIMATION_SPEED  # Animation speed setting
        self.map = game_map  # Reference to the game map
        self.attacking = False  # Attack state
        self.attack_duration = 0.4  # Attack lasts for 0.4 seconds
        self.attack_timer = 0  # Timer for attack duration

        # Load animations for different states
        self.image_idle = self.load_all_images('idle_animation', 3)
        self.image_run = self.load_all_images('run_animation', 4)
        self.image_attack = self.load_all_images('attack_animation', 4)

    def load_all_images(self, action, frames, size=(64, 64)):
        """Load animation frames for different directions."""
        return {
            'down': [pygame.transform.scale(pygame.image.load(f'{action}/hero_down/hero_down_{i+1}.png'), size) for i in range(frames)],
            'left': [pygame.transform.scale(pygame.image.load(f'{action}/hero_left/hero_left_{i+1}.png'), size) for i in range(frames)],
            'right': [pygame.transform.scale(pygame.image.load(f'{action}/hero_right/hero_right_{i+1}.png'), size) for i in range(frames)],
            'up': [pygame.transform.scale(pygame.image.load(f'{action}/hero_up/hero_up_{i+1}.png'), size) for i in range(frames)]
        }

    def can_move(self, new_x, new_y):
        """Check if the player can move to the new position."""
        tile_x = new_x // SCALED_TILE_SIZE
        tile_y = new_y // SCALED_TILE_SIZE
        return not self.map.is_obstacle(tile_x, tile_y)

    def update(self, delta_time, keys):
        """Update player position, attack state, and animation."""
        new_x, new_y = self.x, self.y  # Store potential new position

        if keys[pygame.K_k] and not self.attacking:
            self.attacking = True
            self.attack_timer = self.attack_duration
            self.current_frame = 0  # Reset animation frame
            return  # Prevent movement during attack

        if self.attacking:
            self.attack_timer -= delta_time
            if self.attack_timer <= 0:
                self.attacking = False

        if not self.attacking:
            if keys[pygame.K_LEFT] or keys[pygame.K_q]:
                self.direction = 1
                new_x -= self.speed * delta_time
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.direction = 2
                new_x += self.speed * delta_time
            elif keys[pygame.K_UP] or keys[pygame.K_z]:
                self.direction = 3
                new_y -= self.speed * delta_time
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.direction = 0
                new_y += self.speed * delta_time

            if self.can_move(new_x, new_y):
                self.x, self.y = new_x, new_y
                self.map.update_camera(self)

        self.animation_timer += delta_time
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % 4  # Loop through animation frames

    def draw(self, screen):
        """Draw the correct animation frame based on player state."""
        directions = ['down', 'left', 'right', 'up']
        direction = directions[self.direction]
        
        if self.attacking:
            screen.blit(self.image_attack[direction][self.current_frame], (self.x - self.map.camera_x, self.y - self.map.camera_y))
        else:
            keys = pygame.key.get_pressed()
            if any([keys[pygame.K_LEFT], keys[pygame.K_q], keys[pygame.K_RIGHT], keys[pygame.K_d], 
                    keys[pygame.K_UP], keys[pygame.K_z], keys[pygame.K_DOWN], keys[pygame.K_s]]):
                screen.blit(self.image_run[direction][self.current_frame], (self.x - self.map.camera_x, self.y - self.map.camera_y))
            else:
                screen.blit(self.image_idle[direction][self.current_frame % 3], (self.x - self.map.camera_x, self.y - self.map.camera_y))