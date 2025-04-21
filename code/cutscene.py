import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, SCALED_TILE_SIZE
from Fire import Fire

class Knight:
    """A knight character that can be programmatically controlled with animations."""
    def __init__(self, x, y, run_image_paths, idle_image_paths, knight_id):
        self.x = x
        self.y = y
        self.knight_id = knight_id  # Unique identifier for each knight
        self.speed = 10
        self.target_x = x  # Target position to move towards
        self.target_y = y
        self.is_active = False  # Whether this knight is currently moving
        
        # Load animation frames for running and idle states
        self.run_frames = [
            pygame.transform.scale(pygame.image.load(path), (64, 64))
            for path in run_image_paths
        ]
        
        self.idle_frames = [
            pygame.transform.scale(pygame.image.load(path), (64, 64))
            for path in idle_image_paths
        ]
        
        self.current_frames = self.idle_frames  # Start with idle animation
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.1  # Time (in seconds) per frame
        
    def move_to(self, target_x, target_y):
        """Set a target position for the knight to move towards."""
        self.target_x = target_x
        self.target_y = target_y
        self.is_active = True
        self.current_frames = self.run_frames  # Switch to running animation
        
    def is_at_target(self):
        """Check if the knight has reached its target position."""
        return (abs(self.x - self.target_x) < 5 and 
                abs(self.y - self.target_y) < 5)
        
    def update(self, delta_time):
        """Update knight position and animation."""
        # Handle movement when active
        if self.is_active:
            # Move towards target
            if self.x < self.target_x:
                self.x += min(self.speed, self.target_x - self.x)
            elif self.x > self.target_x:
                self.x -= min(self.speed, self.x - self.target_x)
                
            if self.y < self.target_y:
                self.y += min(self.speed, self.target_y - self.y)
            elif self.y > self.target_y:
                self.y -= min(self.speed, self.y - self.target_y)
            
            # If knight has reached target, mark as inactive and switch to idle animation
            if self.is_at_target():
                self.is_active = False
                self.current_frames = self.idle_frames
                self.current_frame = 0  # Reset animation frame
        
        # Update animation
        self.animation_timer += delta_time
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.current_frames)
            
    def draw(self, screen, camera_x, camera_y):
        """Draw the knight to the screen."""
        current_image = self.current_frames[self.current_frame]
        screen.blit(current_image, (self.x - camera_x, self.y - camera_y))
        
class Cutscene:
    """Handles the game's cutscenes with programmatically controllable knights."""
    def __init__(self, game_map):
        self.map = game_map
        self.is_playing = False
        self.step_timer = 0
        self.cutscene_duration = 15.0  # Duration in seconds before the cutscene ends
        self.fires = []  # List to store fire objects
        self.camera_x, self.camera_y = 0, 0
        self.camera_target_x, self.camera_target_y = 0, 0
        self.camera_speed = 3
        
        # Calculate map boundaries for camera
        self.map_width = self.map.visible_width * SCALED_TILE_SIZE
        self.map_height = self.map.visible_height * SCALED_TILE_SIZE
        
        # Load knight images
        self.knight_run_left_images = [
            'knight_run/knight_run_left/knight_run_left_1.png',
            'knight_run/knight_run_left/knight_run_left_2.png',
            'knight_run/knight_run_left/knight_run_left_3.png',
            'knight_run/knight_run_left/knight_run_left_4.png'
        ]
        
        self.knight_idle_images = [
            'knight_idle/knight_idle_left/knight_idle_left_1.png',
            'knight_idle/knight_idle_left/knight_idle_left_2.png',
            'knight_idle/knight_idle_left/knight_idle_left_3.png'
        ]
        
        # Initialize knights with different positions
        self.knights = []
        for i in range(6):
            knight_x = self.map_width - 100 # Staggered positions horizontally
            knight_y = min(self.map_height - 100, 100 + (i * 20))  # Staggered positions vertically
            
            knight = Knight(
                knight_x,
                knight_y,
                self.knight_run_left_images,
                self.knight_idle_images,
                knight_id=i  # Assign unique ID
            )
            self.knights.append(knight)
        
        # Cutscene state management
        self.cutscene_steps = []
        self.current_step = 0
        
        # Fire destinations that correspond to knight destinations
        self.fire_locations = [
            (self.map_width - 1020, 250),  # Near knight 0's destination
            (self.map_width - 720, 650),   # Near knight 1's destination
            (self.map_width - 720, 250)    # Near knight 2's destination
        ]

        # Additional fire locations on top of knights (2 large fires)
        self.large_fire_locations = [
            (self.map_width - 980, 200),  # Above and beside knight 0
            (self.map_width - 680, 600),   # Near knight 1's destination
            (self.map_width - 680, 200)   # Above and beside knight 2
        ]
    
    def start(self):
        """Start the cutscene mode."""
        self.is_playing = True
        self.step_timer = 0
        # Initial camera position (center of the map)
        self.camera_x = self.map_width - 100
        self.camera_y = min(self.map_height - 100, 100) 
        
        # Define cutscene steps
        self.cutscene_steps = [
            # Each entry is (time_trigger, function, args)
            (0.5, self.move_knight, (0, self.map_width - 1000, 250)),
            (1.0, self.move_knight, (1, self.map_width - 700, 650)),
            (1.5, self.move_knight, (2, self.map_width - 700, 250)),
            (2.0, self.set_camera_position, (self.map_width - 1500, 0)),
            # Add fire creation steps when knights reach their destinations
            (3.0, self.check_and_create_fires, ()),
            (3.5, self.check_and_create_large_fires, ()),
            (4.0, self.check_and_create_fires, ()),
            (4.5, self.check_and_create_large_fires, ()),
            (5.0, self.check_and_create_fires, ()),
            (5.5, self.check_and_create_large_fires, ()),
            (6.0, self.check_and_create_fires, ()),
            (6.5, self.check_and_create_large_fires, ()),
            # After all knights reach their destinations and we've waited a bit, end the cutscene
            (7.5, self.end_cutscene, ())
        ]
        
        self.current_step = 0
        self.clamp_camera()
    
    def check_and_create_fires(self):
        """Check which knights have arrived and create fires next to them."""
        for i in range(3):  # We have 3 fire locations corresponding to the first 3 knights
            if self.knight_arrived(i) and i < len(self.fire_locations):
                # Check if a fire already exists at this location
                fire_exists = False
                for fire in self.fires:
                    if (abs(fire.x - self.fire_locations[i][0]) < 10 and 
                        abs(fire.y - self.fire_locations[i][1]) < 10):
                        fire_exists = True
                        break
                
                # If no fire exists at this location, create one
                if not fire_exists:
                    fire_x, fire_y = self.fire_locations[i]
                    self.fires.append(Fire(fire_x, fire_y, scale=1.25))

    def check_and_create_large_fires(self):
        """Create larger fires above knights 0 and 2 when they arrive."""
        # Check for knight 0
        if self.knight_arrived(0):
            # Check if a large fire already exists at location 0
            large_fire_exists = False
            for fire in self.fires:
                if (abs(fire.x - self.large_fire_locations[0][0]) < 10 and 
                    abs(fire.y - self.large_fire_locations[0][1]) < 10 and
                    fire.scale > 2.0):  # Check if it's a large fire
                    large_fire_exists = True
                    break
            
            # If no large fire exists at this location, create one
            if not large_fire_exists:
                fire_x, fire_y = self.large_fire_locations[0]
                self.fires.append(Fire(fire_x, fire_y, scale=3.0))  # 3x larger
        # Check for knight 
        if self.knight_arrived(1):
            # Check if a large fire already exists at location 1
            large_fire_exists = False
            for fire in self.fires:
                if (abs(fire.x - self.large_fire_locations[1][0]) < 10 and 
                    abs(fire.y - self.large_fire_locations[1][1]) < 10 and
                    fire.scale > 2.0):  # Check if it's a large fire
                    large_fire_exists = True
                    break

            # If no large fire exists at this location, create one
            if not large_fire_exists:
                fire_x, fire_y = self.large_fire_locations[1]
                self.fires.append(Fire(fire_x, fire_y, scale=3.0))  # 3x larger
        # Check for knight 2
        if self.knight_arrived(2):
            # Check if a large fire already exists at location 1
            large_fire_exists = False
            for fire in self.fires:
                if (abs(fire.x - self.large_fire_locations[2][0]) < 10 and 
                    abs(fire.y - self.large_fire_locations[2][1]) < 10 and
                    fire.scale > 2.0):  # Check if it's a large fire
                    large_fire_exists = True
                    break

            # If no large fire exists at this location, create one
            if not large_fire_exists:
                fire_x, fire_y = self.large_fire_locations[1]
                self.fires.append(Fire(fire_x, fire_y, scale=3.0))  # 3x larger
    
    def clamp_camera(self):
        """Ensure camera stays within map boundaries."""
        self.camera_x = max(0, min(self.camera_x, self.map_width - SCREEN_WIDTH))
        self.camera_y = max(0, min(self.camera_y, self.map_height - SCREEN_HEIGHT))
    
    def move_knight(self, knight_id, target_x, target_y):
        """Move a specific knight to the target position."""
        if 0 <= knight_id < len(self.knights):
            self.knights[knight_id].move_to(target_x, target_y)
    
    def focus_camera_on_knight(self, knight_id):
        """Center the camera on a specific knight."""
        if 0 <= knight_id < len(self.knights):
            knight = self.knights[knight_id]
            self.camera_target_x = knight.x - SCREEN_WIDTH // 2
            self.camera_target_y = knight.y - SCREEN_HEIGHT // 2
            self.clamp_camera()
    
    def set_camera_position(self, x, y):
        """Set the camera to a specific position."""
        self.camera_target_x = x
        self.camera_target_y = y
        self.clamp_camera()
    
    def all_knights_arrived(self):
        """Check if all knights have reached their targets."""
        return all(not knight.is_active for knight in self.knights)
    
    def knight_arrived(self, knight_id):
        """Check if a specific knight has reached its target."""
        if 0 <= knight_id < len(self.knights):
            return not self.knights[knight_id].is_active
        return False
    
    def update(self, delta_time):
        """Update the cutscene state and all knights."""
        if not self.is_playing:
            return False
            
        self.step_timer += delta_time
        
        # Execute cutscene steps based on timer
        while (self.current_step < len(self.cutscene_steps) and 
               self.step_timer >= self.cutscene_steps[self.current_step][0]):
            time_trigger, function, args = self.cutscene_steps[self.current_step]
            function(*args)
            self.current_step += 1
        
        # End cutscene if all knights have arrived and steps are complete
        if (self.all_knights_arrived() and 
            self.current_step >= len(self.cutscene_steps) and 
            self.step_timer >= self.cutscene_duration):
            self.is_playing = False
        
        # Update all knights independently
        for knight in self.knights:
            knight.update(delta_time)
            
            # Keep knights within map boundaries
            knight.x = max(0, min(knight.x, self.map_width - 64))
            knight.y = max(0, min(knight.y, self.map_height - 64))
        
        # Update all fires
        for fire in self.fires:
            fire.update(delta_time)
        
        # Update camera position
        if self.camera_x < self.camera_target_x:
            self.camera_x += min(self.camera_speed, self.camera_target_x - self.camera_x)
        elif self.camera_x > self.camera_target_x:
            self.camera_x -= min(self.camera_speed, self.camera_x - self.camera_target_x)
            
        if self.camera_y < self.camera_target_y:
            self.camera_y += min(self.camera_speed, self.camera_target_y - self.camera_y)
        elif self.camera_y > self.camera_target_y:
            self.camera_y -= min(self.camera_speed, self.camera_y - self.camera_target_y)
        
        # Keep camera within map boundaries
        self.clamp_camera()
        
        return False
    
    def end_cutscene(self):
        """End the cutscene mode."""
        self.is_playing = False
        return True
        
    def draw(self, screen):
        """Draw the cutscene with all knights and fires."""
        # Draw the map background
        self.map.draw(screen, self.camera_x, self.camera_y)
        
        # Draw all fires behind knights for better layering
        for fire in self.fires:
            fire.draw(screen, self.camera_x, self.camera_y)
            
        # Draw all knights
        for knight in self.knights:
            knight.draw(screen, self.camera_x, self.camera_y)