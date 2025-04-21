import pygame
import math
from enemy_bot import Enemy

class KnightEnemy(Enemy):
    """A knight enemy that moves around the map and attacks when player enters its radius."""
    def __init__(self, x, y, knight_id):
        # Position and identification
        self.knight_id = knight_id  # Unique identifier for each knight
        
        # Create a rect for collision and positioning
        self.rect = pygame.Rect(x, y, 64, 64)
        
        # Movement parameters
        self.attack_radius = 100  # Reduced from 150 to 100 for detection radius
        self.patrol_radius = 250  # Radius for patrol movement
        self.patrol_points = self.generate_patrol_points(x, y)
        self.current_patrol_index = 0
        self.target_x = self.patrol_points[0][0]
        self.target_y = self.patrol_points[0][1]
        self.movement_speed = 3
        self.Flip = False
        
        # Combat parameters
        self.attack_move = False
        self.attacking = False
        self.attack_cooldown = 0
        self.attack_cooldown_max = 60  # Frames until knight can attack again
        self.running = False
        self.dead = False
        self.health = 100
        
        # Animation parameters
        self.update_time = pygame.time.get_ticks()
        self.frame_index = 0
        self.action = 0  # 0:idle, 1:run, 2:attack
        self.animation_speed = 0.1  # Time in seconds per frame
        
        # Load knight images - using the same images from cutscene Knight class
        self.run_frames = [
            pygame.transform.scale(pygame.image.load(path), (64, 64))
            for path in [
                'knight_run/knight_run_left/knight_run_left_1.png',
                'knight_run/knight_run_left/knight_run_left_2.png',
                'knight_run/knight_run_left/knight_run_left_3.png',
                'knight_run/knight_run_left/knight_run_left_4.png'
            ]
        ]
        
        self.idle_frames = [
            pygame.transform.scale(pygame.image.load(path), (64, 64))
            for path in [
                'knight_idle/knight_idle_left/knight_idle_left_1.png',
                'knight_idle/knight_idle_left/knight_idle_left_2.png',
                'knight_idle/knight_idle_left/knight_idle_left_3.png'
            ]
        ]
        
        # Attack frames - needs to be created with appropriate attack animation images
        self.attack_frames = [
            pygame.transform.scale(pygame.image.load(path), (64, 64))
            for path in [
                'knight_run/knight_run_left/knight_run_left_1.png',
                'knight_run/knight_run_left/knight_run_left_2.png',
                'knight_run/knight_run_left/knight_run_left_3.png',
                'knight_run/knight_run_left/knight_run_left_4.png'
            ]
        ]
        
        # Death frames
        self.death_frames = [
            pygame.transform.scale(pygame.image.load(path), (64, 64))
            for path in [
                'knight_idle/knight_idle_left/knight_idle_left_1.png',
                'knight_idle/knight_idle_left/knight_idle_left_2.png',
                'knight_idle/knight_idle_left/knight_idle_left_3.png'
            ]
        ]
        
        # Animation lists for different actions
        self.animation_list = [
            self.idle_frames,   # Action 0: Idle
            self.run_frames,    # Action 1: Run
            self.attack_frames, # Action 2: Attack
            self.death_frames   # Action 3: Death
        ]
        
        # Current image
        self.image = self.idle_frames[0]
        
    def generate_patrol_points(self, center_x, center_y):
        """Generate points for the knight to patrol around."""
        points = []
        # Create a square patrol pattern
        points.append((center_x, center_y))  # Start position
        points.append((center_x + self.patrol_radius, center_y))
        points.append((center_x + self.patrol_radius, center_y + self.patrol_radius))
        points.append((center_x, center_y + self.patrol_radius))
        return points
        
    def move_to_next_patrol_point(self):
        """Move to the next patrol point in the sequence."""
        self.current_patrol_index = (self.current_patrol_index + 1) % len(self.patrol_points)
        self.target_x, self.target_y = self.patrol_points[self.current_patrol_index]
        
    def is_at_target(self):
        """Check if the knight has reached its target position."""
        return (abs(self.rect.x - self.target_x) < 10 and 
                abs(self.rect.y - self.target_y) < 10)
    
    def update_action(self, new_action):
        """Change the current animation."""
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
                
    def update(self, delta_time, target):
        """Update knight position, animation, and attack state."""
        # Handle attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            
        # Don't update if dead
        if self.dead:
            self.update_action(3)  # Death animation
            # Stay on last frame of death animation
            if self.frame_index >= len(self.animation_list[3]) - 1:
                self.frame_index = len(self.animation_list[3]) - 1
            return
            
        # Calculate distance to player
        distance_to_player = math.sqrt((target.rect.centerx - self.rect.centerx)**2 + 
                                      (target.rect.centery - self.rect.centery)**2)
        
        # Check if player is within follow radius (100 units)
        if distance_to_player <= self.attack_radius and not target.dead:
            # Face the player
            if target.rect.centerx < self.rect.centerx:
                self.Flip = True
            else:
                self.Flip = False
                
            # Move towards player
            self.move_towards(target.rect.centerx, target.rect.centery)
            self.update_action(1)  # Running animation
            
            # Check if close enough to attack (within 50 units)
            if distance_to_player <= 50 and self.attack_cooldown == 0:
                self.attack_move = True
                self.attacking = True
                self.update_action(2)  # Attack animation
                self.attack(target)
                self.attack_cooldown = self.attack_cooldown_max
        else:
            # Patrol behavior when player is not in range
            self.attack_move = False
            self.attacking = False
            
            if self.is_at_target():
                self.move_to_next_patrol_point()
                
            # Move towards patrol point
            self.move_towards(self.target_x, self.target_y)
            
            # Update animation based on movement
            if abs(self.rect.x - self.target_x) > 5 or abs(self.rect.y - self.target_y) > 5:
                self.update_action(1)  # Running animation
            else:
                self.update_action(0)  # Idle animation
        
        # Update animation frame
        animation_cooldown = self.animation_speed * 1000  # Convert to milliseconds
        
        # Current time
        current_time = pygame.time.get_ticks()
        
        # Update animation frame if enough time has passed
        if current_time - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = current_time
            
            # Loop animation unless it's death animation
            if self.frame_index >= len(self.animation_list[self.action]):
                if self.action == 3:  # Death animation
                    self.frame_index = len(self.animation_list[self.action]) - 1
                else:
                    self.frame_index = 0
                    # Reset attacking state when attack animation completes
                    if self.action == 2:  # Attack animation
                        self.attacking = False
    
    def move_towards(self, target_x, target_y):
        """Move towards a target position."""
        # Calculate direction vector
        dx = target_x - self.rect.centerx
        dy = target_y - self.rect.centery
        distance = max(1, math.sqrt(dx**2 + dy**2))  # Avoid division by zero
        
        # Normalize and scale by speed
        dx = (dx / distance) * self.movement_speed
        dy = (dy / distance) * self.movement_speed
        
        # Update position
        self.rect.x += dx
        self.rect.y += dy
        
        # Set flip based on movement direction
        if dx < 0:
            self.Flip = True
        elif dx > 0:
            self.Flip = False
            
    def attack(self, target):
        """Attack the target if in range."""
        # Define attack hitbox based on knight's orientation
        if self.Flip:  # Facing left
            attack_rect = pygame.Rect(self.rect.x - 40, self.rect.y, 40, self.rect.height)
        else:  # Facing right
            attack_rect = pygame.Rect(self.rect.right, self.rect.y, 40, self.rect.height)
            
        # Check collision with player
        if attack_rect.colliderect(target.rect) and self.attacking:
            target.health -= 10  # Deal damage to player
            
    def draw(self, surface):
        """Draw the knight to the screen."""
        # Get current animation frame
        current_frame = self.animation_list[self.action][self.frame_index]
        
        # Flip image if necessary
        image = pygame.transform.flip(current_frame, self.Flip, False)
        
        # Draw knight
        surface.blit(image, self.rect.topleft)