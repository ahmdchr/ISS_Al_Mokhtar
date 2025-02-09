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
        self.attacking = False  # Attack state
        self.attack_duration = 0.4  # Attack lasts for 0.4 seconds
        self.attack_timer = 0  

        # Load animations
        self.image_idle_down = self.load_images('idle_animation/hero_down/hero_down_', 3)
        self.image_idle_left = self.load_images('idle_animation/hero_left/hero_left_', 3)
        self.image_idle_right = self.load_images('idle_animation/hero_right/hero_right_', 3)
        self.image_idle_up = self.load_images('idle_animation/hero_up/hero_up_', 3)

        self.image_run_down = self.load_images('run_animation/hero_down/hero_down_', 4)
        self.image_run_left = self.load_images('run_animation/hero_left/hero_left_', 4)
        self.image_run_right = self.load_images('run_animation/hero_right/hero_right_', 4)
        self.image_run_up = self.load_images('run_animation/hero_up/hero_up_', 4)

        self.image_attack_down = self.load_images('attack_animation/hero_down/hero_down_', 4)
        self.image_attack_left = self.load_images('attack_animation/hero_left/hero_left_', 4)
        self.image_attack_right = self.load_images('attack_animation/hero_right/hero_right_', 4)
        self.image_attack_up = self.load_images('attack_animation/hero_up/hero_up_', 4)

    def load_images(self, path, frames, size=(64, 64)):
        return [pygame.transform.scale(pygame.image.load(f"{path}{i+1}.png"), size) for i in range(frames)]

    def can_move(self, new_x, new_y):
        """Check if the player can move to (new_x, new_y) without hitting an obstacle."""
        tile_x = new_x // SCALED_TILE_SIZE
        tile_y = new_y // SCALED_TILE_SIZE
        return not self.map.is_obstacle(tile_x, tile_y)

    def update(self, deltaTime, keys):
        new_x, new_y = self.x, self.y  # Store potential new position

        # Handle attack
        if keys[pygame.K_k] and not self.attacking:
            self.attacking = True
            self.attack_timer = self.attack_duration
            self.current_frame = 0  # Reset animation frame
            return  # Prevent movement during attack

        # Update attack timer
        if self.attacking:
            self.attack_timer -= deltaTime
            if self.attack_timer <= 0:
                self.attacking = False

        # Handle movement only if not attacking
        if not self.attacking:
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

        # Move the camera to follow the player
        self.map.update_camera(self.x, self.y)

        # Update animation frame
        self.animation_timer += deltaTime
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % 4  # 4 frames for attack and run animations


    def draw(self, screen):
        if self.attacking:
            if self.direction == 0:
                screen.blit(self.image_attack_down[self.current_frame], (self.x, self.y))
            elif self.direction == 1:
                screen.blit(self.image_attack_left[self.current_frame], (self.x, self.y))
            elif self.direction == 2:
                screen.blit(self.image_attack_right[self.current_frame], (self.x, self.y))
            elif self.direction == 3:
                screen.blit(self.image_attack_up[self.current_frame], (self.x, self.y))
        else:
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
