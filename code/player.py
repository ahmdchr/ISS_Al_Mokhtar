import pygame
from settings import PLAYER_SPEED, ANIMATION_SPEED, SCALED_TILE_SIZE

class Player:
    def __init__(self, game_map):
        self.x, self.y = 300, 300
        self.direction = 0  # 0: down, 1: left, 2: right, 3: up
        self.current_frame = 0
        self.animation_timer = 0
        self.speed = PLAYER_SPEED
        self.animation_speed = ANIMATION_SPEED
        self.map = game_map  # Reference to the map

        # Load player animations
        self.image_idle_down = self.load_images('idle_animation/hero_down/hero_down_', 3)
        self.image_idle_left = self.load_images('idle_animation/hero_left/hero_left_', 3)
        self.image_idle_right = self.load_images('idle_animation/hero_right/hero_right_', 3)
        self.image_idle_up = self.load_images('idle_animation/hero_up/hero_up_', 3)

        self.image_run_down = self.load_images('run_animation/hero_down/hero_down_', 4)
        self.image_run_left = self.load_images('run_animation/hero_left/hero_left_', 4)
        self.image_run_right = self.load_images('run_animation/hero_right/hero_right_', 4)
        self.image_run_up = self.load_images('run_animation/hero_up/hero_up_', 4)

    def load_images(self, path, frames, size=(64, 64)):
        return [pygame.transform.scale(pygame.image.load(f"{path}{i+1}.png"), size) for i in range(frames)]

    def can_move(self, new_x, new_y):
        """Check if the player can move to (new_x, new_y) without hitting an obstacle."""
        tile_x = new_x // SCALED_TILE_SIZE
        tile_y = new_y // SCALED_TILE_SIZE
        return not self.map.is_obstacle(tile_x, tile_y)

    def update(self, deltaTime, keys):
        new_x, new_y = self.x, self.y  # Store potential new position

        if keys[pygame.K_LEFT] or keys[pygame.K_q]:
            self.direction = 1
            new_x -= self.speed * deltaTime
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction = 2
            new_x += self.speed * deltaTime
        elif keys[pygame.K_UP] or keys[pygame.K_z]:
            self.direction = 3
            new_y -= self.speed * deltaTime
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction = 0
            new_y += self.speed * deltaTime

        # Only update position if it's not an obstacle
        if self.can_move(new_x, new_y):
            self.x, self.y = new_x, new_y

        # Update animation frame
        self.animation_timer += deltaTime
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % 4  # Assuming 4 frames for running animations

    def draw(self, screen):
        keys = pygame.key.get_pressed()
        if any([keys[pygame.K_LEFT], keys[pygame.K_q], keys[pygame.K_RIGHT], keys[pygame.K_d], 
                keys[pygame.K_UP], keys[pygame.K_z], keys[pygame.K_DOWN], keys[pygame.K_s]]):
            # Running animation
            if self.direction == 0:
                screen.blit(self.image_run_down[self.current_frame], (self.x, self.y))
            elif self.direction == 1:
                screen.blit(self.image_run_left[self.current_frame], (self.x, self.y))
            elif self.direction == 2:
                screen.blit(self.image_run_right[self.current_frame], (self.x, self.y))
            elif self.direction == 3:
                screen.blit(self.image_run_up[self.current_frame], (self.x, self.y))
        else:
            # Idle animation
            if self.direction == 0:
                screen.blit(self.image_idle_down[self.current_frame % 3], (self.x, self.y))
            elif self.direction == 1:
                screen.blit(self.image_idle_left[self.current_frame % 3], (self.x, self.y))
            elif self.direction == 2:
                screen.blit(self.image_idle_right[self.current_frame % 3], (self.x, self.y))
            elif self.direction == 3:
                screen.blit(self.image_idle_up[self.current_frame % 3], (self.x, self.y))
