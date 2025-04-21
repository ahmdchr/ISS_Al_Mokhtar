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
        
        # Health system
        self.health = 100  # Player's health
        self.max_health = 100  # Maximum health
        self.dead = False  # Death state
        
        # Create a rect for collision detection
        self.rect = pygame.Rect(self.x, self.y, 64, 64)  # Size based on sprite size
        
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
        # Check if player is dead
        if self.health <= 0:
            self.dead = True
            return  # Don't process anything else if dead
            
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

        if not self.attacking and not self.dead:
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
                # Update rect for collision detection
                self.rect.x = self.x
                self.rect.y = self.y
                self.map.update_camera(self)

        self.animation_timer += delta_time
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % 4  # Loop through animation frames
            
    def attack_check(self, enemies):
        """Check if player's attack hits enemies"""
        if not self.attacking:
            return
            
        # Create an attack hitbox based on direction
        attack_rect = None
        offset = 40  # Distance in front of player for attack hitbox
        
        if self.direction == 0:  # Down
            attack_rect = pygame.Rect(self.x, self.y + offset, 64, 40)
        elif self.direction == 1:  # Left
            attack_rect = pygame.Rect(self.x - offset, self.y, 40, 64)
        elif self.direction == 2:  # Right
            attack_rect = pygame.Rect(self.x + offset, self.y, 40, 64)
        elif self.direction == 3:  # Up
            attack_rect = pygame.Rect(self.x, self.y - offset, 64, 40)
            
        # Check collision with enemies
        for enemy in enemies:
            if attack_rect.colliderect(enemy.rect) and not enemy.dead:
                enemy.health -= 20  # Damage value
                if enemy.health <= 0:
                    enemy.dead = True

    def draw(self, screen):
        """Draw the correct animation frame based on player state."""
        if self.dead:
            # Draw dead state - could use a specific death animation
            # For now, just use the first idle frame with red tint
            directions = ['down', 'left', 'right', 'up']
            direction = directions[self.direction]
            dead_img = self.image_idle[direction][0].copy()
            # Apply red tint to indicate death
            red_overlay = pygame.Surface(dead_img.get_size(), pygame.SRCALPHA)
            red_overlay.fill((255, 0, 0, 128))  # semi-transparent red
            dead_img.blit(red_overlay, (0, 0))
            screen.blit(dead_img, (self.x - self.map.camera_x, self.y - self.map.camera_y))
            return
            
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
                
        # Debug: draw player's collision rect
        # pygame.draw.rect(screen, (255, 0, 0), 
        #                 (self.rect.x - self.map.camera_x, self.rect.y - self.map.camera_y, 
        #                  self.rect.width, self.rect.height), 1)