import pygame

class Fire:
    """
    A class to create animated fire effects that can be placed anywhere on the map.
    """
    def __init__(self, x, y, scale=1.0, permanent=True):
        """
        Initialize a fire animation at the specified position.
        
        Args:
            x (int): X-coordinate of the fire
            y (int): Y-coordinate of the fire
            scale (float): Scale factor for the fire size (default: 1.0)
            permanent (bool): If True, fire burns forever; if False, it extinguishes after duration
        """
        self.x = x
        self.y = y
        self.scale = scale
        self.permanent = permanent
        self.active = True
        
        # Load fire animation frames - you'll need to create these images
        try:
            self.frames = []
            for i in range(1, 5):  # Assuming you have fire_1.png through fire_4.png
                image = pygame.image.load(f'fire/burning_loop_{i}.png')
                # Scale the image based on the scale factor
                width = int(image.get_width() * scale)
                height = int(image.get_height() * scale)
                scaled_image = pygame.transform.scale(image, (width, height))
                self.frames.append(scaled_image)
        except pygame.error:
            # If images can't be loaded, create placeholder colored rectangles
            print("Warning: Fire images not found. Using placeholder rectangles.")
            colors = [(255, 0, 0), (255, 60, 0), (255, 120, 0), (255, 200, 0)]  # Red to yellow
            size = int(64 * scale)
            self.frames = []
            for color in colors:
                surface = pygame.Surface((size, size), pygame.SRCALPHA)
                pygame.draw.rect(surface, color, (0, 0, size, size))
                self.frames.append(surface)
        
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.1  # Time (in seconds) per frame
        
        # Only used if permanent is False
        self.duration = 3.0  # Fire lasts for 3 seconds if not permanent
        self.elapsed_time = 0
        
        # Add some variation with flickering
        self.flicker_timer = 0
        self.flicker_speed = 0.5  # How often the fire might flicker
        self.visible = True
        
    def update(self, delta_time):
        """
        Update fire animation state.
        
        Args:
            delta_time (float): Time elapsed since last update in seconds
        """
        if not self.active:
            return
            
        # Update animation frame
        self.animation_timer += delta_time
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
        
        # Add flickering effect
        self.flicker_timer += delta_time
        if self.flicker_timer >= self.flicker_speed:
            self.flicker_timer = 0
            # 10% chance to flicker
            if pygame.time.get_ticks() % 10 == 0:
                self.visible = not self.visible
            else:
                self.visible = True
        
        # Check if non-permanent fire should be extinguished    
        if not self.permanent:
            self.elapsed_time += delta_time
            if self.elapsed_time >= self.duration:
                self.active = False
    
    def set_position(self, x, y):
        """Update the position of the fire."""
        self.x = x
        self.y = y
            
    def draw(self, screen, camera_x=0, camera_y=0):
        """
        Draw the fire effect on screen.
        
        Args:
            screen: Pygame surface to draw on
            camera_x (int): Camera X offset
            camera_y (int): Camera Y offset
        """
        if not self.active or not self.visible:
            return
            
        current_image = self.frames[self.current_frame]
        # Get dimensions for positioning
        width = current_image.get_width()
        height = current_image.get_height()
        
        # Draw fire with correct position accounting for camera offset
        screen.blit(current_image, (self.x - camera_x, self.y - camera_y - height))
    
    def extinguish(self):
        """Immediately extinguish the fire."""
        self.active = False


# Example usage:
"""
# In your game initialization:
fires = []
fires.append(Fire(200, 300))  # Add permanent fire at position (200, 300)
fires.append(Fire(400, 500, scale=1.5, permanent=False))  # Add larger temporary fire

# In your game loop:
for fire in fires:
    fire.update(delta_time)
    
# In your drawing code:
for fire in fires:
    fire.draw(screen, camera_x, camera_y)

# Remove extinguished fires:
fires = [fire for fire in fires if fire.active]
"""