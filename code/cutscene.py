import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, SCALED_TILE_SIZE

class Knight:
    """A simple knight character for the cutscene with animations."""
    def __init__(self, x, y, image_paths):
        self.x = x
        self.y = y
        self.target_x = 0
        self.target_y = 0
        self.speed = 2
        
        # Load animation frames
        self.animation_frames = [
            pygame.transform.scale(pygame.image.load(path), (64, 64))
            for path in image_paths
        ]
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.1  # Time (in seconds) per frame
        
    def move_to(self, target_x, target_y):
        """Set a target position for the knight to move towards."""
        self.target_x = target_x
        self.target_y = target_y
        
    def update(self, delta_time):
        """Move the knight towards their target position and update animation."""
        # Update position
        if self.x < self.target_x:
            self.x += min(self.speed, self.target_x - self.x)
        elif self.x > self.target_x:
            self.x -= min(self.speed, self.x - self.target_x)
            
        if self.y < self.target_y:
            self.y += min(self.speed, self.target_y - self.y)
        elif self.y > self.target_y:
            self.y -= min(self.speed, self.y - self.target_y)
        
        # Update animation
        self.animation_timer += delta_time
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.animation_frames)
            
    def draw(self, screen, camera_x, camera_y):
        """Draw the knight to the screen."""
        current_image = self.animation_frames[self.current_frame]
        screen.blit(current_image, (self.x - camera_x, self.y - camera_y))

class Cutscene:
    """Handles the game's cutscenes."""
    def __init__(self, game_map):
        self.map = game_map
        self.is_playing = False
        self.current_step = 0
        self.step_timer = 0
        self.knights = []
        
        # Set initial player position to match where they'll spawn in gameplay
        self.player_x, self.player_y = 300, 300  # Same starting position as in player.py
        self.sister_x, self.sister_y = 350, 300  # Sister positioned to the right of player
        
        self.camera_x, self.camera_y = 0, 0
        self.camera_target_x, self.camera_target_y = 0, 0
        self.camera_speed = 3
        
        # Calculate map boundaries for camera
        self.map_width = self.map.visible_width * SCALED_TILE_SIZE
        self.map_height = self.map.visible_height * SCALED_TILE_SIZE
        
        # Load knight images
        self.knight_images = [
            'knight_run/knight_run_left/knight_run_left_1.png',
            'knight_run/knight_run_left/knight_run_left_2.png',
            'knight_run/knight_run_left/knight_run_left_3.png',
            'knight_run/knight_run_left/knight_run_left_4.png'
               ]
        
        # Scale images to match player size in gameplay (64x64)
        self.player_image = pygame.transform.scale(
            pygame.image.load('idle_animation/hero_down/hero_down_1.png'),
            (64, 64)
        )
        self.sister_image = pygame.transform.scale(
            pygame.image.load('idle_animation/hero_down/hero_down_1.png'),  # Replace with sister image
            (64, 64)
        )
        
        # Load player attack animation frames
        self.player_attack_images = [
            pygame.transform.scale(
                pygame.image.load(f'attack_animation/hero_left/hero_left_{i}.png'),
                (64, 64)
            )
            for i in range(1, 5)  # Assuming 4 frames for the attack animation
        ]
        
        # Initialize knights within the rightmost edge of the map
        for i in range(6):
            # Start from the rightmost edge of the map
            knight_x = self.map_width - 100  # Rightmost edge minus a margin
            knight_y = min(self.map_height - 100, 100 + (i * 20))  # Staggered positions vertically
            
            knight = Knight(
                knight_x,  # Start at the rightmost edge
                knight_y,  # Staggered positions
                self.knight_images  # Pass the list of animation frames
            )
            self.knights.append(knight)
    
    def start(self):
        """Start playing the cutscene."""
        self.is_playing = True
        self.current_step = 0
        self.step_timer = 0
        
        # Reset knight positions to the rightmost edge of the map
        for i, knight in enumerate(self.knights):
            knight_x = self.map_width - 100  # Rightmost edge minus a margin
            knight_y = min(self.map_height - 100, 100 + (i * 20))  # Staggered positions vertically
            knight.x = knight_x
            knight.y = knight_y
        
        # Initial camera position (focus on player)
        self.camera_x = self.player_x - SCREEN_WIDTH // 2
        self.camera_y = self.player_y - SCREEN_HEIGHT // 2
        self.clamp_camera()
        
        # Set knight targets - they'll move toward the player
        for i, knight in enumerate(self.knights):
            knight.move_to(self.player_x + 700 + (i * 30), self.player_y + 500)
    
    def clamp_camera(self):
        """Ensure camera stays within map boundaries."""
        self.camera_x = max(0, min(self.camera_x, self.map_width - SCREEN_WIDTH))
        self.camera_y = max(0, min(self.camera_y, self.map_height - SCREEN_HEIGHT))
    
    def update(self, delta_time):
        """Update the cutscene state."""
        if not self.is_playing:
            return False
            
        self.step_timer += delta_time
        
        # Update knights
        for knight in self.knights:
            knight.update(delta_time)
        
        # Update camera position
        if self.camera_x < self.camera_target_x:
            self.camera_x += min(self.camera_speed+10, self.camera_target_x - self.camera_x)
        elif self.camera_x > self.camera_target_x:
            self.camera_x -= min(self.camera_speed+10, self.camera_x - self.camera_target_x)
            
        if self.camera_y < self.camera_target_y:
            self.camera_y += min(self.camera_speed+10, self.camera_target_y - self.camera_y)
        elif self.camera_y > self.camera_target_y:
            self.camera_y -= min(self.camera_speed+10, self.camera_y - self.camera_target_y)
        
        # Keep camera within map boundaries
        self.clamp_camera()
        
        # Cutscene step logic
        if self.current_step == 0:
            # First focus on knights approaching
            first_knight = self.knights[0]
            self.camera_target_x = first_knight.x - SCREEN_WIDTH//2
            self.camera_target_y = first_knight.y - SCREEN_HEIGHT//2
            
            # Check if knights have reached their positions
            all_knights_arrived = True
            for knight in self.knights:
                if abs(knight.x - knight.target_x) > 5 or abs(knight.y - knight.target_y) > 5:
                    all_knights_arrived = False
                    break
            
            if all_knights_arrived and self.step_timer > 3.0:  # Wait 3 seconds
                self.current_step = 1
                self.step_timer = 0
                # Move camera to player and sister
                self.camera_target_x = self.player_x - SCREEN_WIDTH//2
                self.camera_target_y = self.player_y - SCREEN_HEIGHT//2
                
        elif self.current_step == 1:
            # Hold on player and sister for a moment
            if self.step_timer > 3.0:  # Wait 3 seconds
                self.current_step = 2
                self.step_timer = 0
                
        elif self.current_step == 2:
            # End cutscene
            if self.step_timer > 1.0:
                self.is_playing = False
                return True  # Cutscene is finished
        
        return False  # Cutscene still playing
        
    def draw(self, screen):
        """Draw the cutscene."""
        # Draw the map background
        self.map.draw(screen, self.camera_x, self.camera_y)
        
        # Draw player and sister
        screen.blit(self.player_image, (self.player_x - self.camera_x, self.player_y - self.camera_y))
        screen.blit(self.sister_image, (self.sister_x - self.camera_x, self.sister_y - self.camera_y))
        
        # Draw knights
        for knight in self.knights:
            knight.draw(screen, self.camera_x, self.camera_y)