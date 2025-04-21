import pygame

class HealthBar:
    """A simple health bar to display the player's health."""
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health
        self.width = 200
        self.height = 20
        # Add a small animation for health changes
        self.displayed_health = health  # Current displayed health value
        self.health_change_speed = 3  # Speed at which the displayed health updates
        
    def update(self, current_health):
        """Update the health value with smooth animation."""
        # Clamp health value between 0 and max_health
        self.health = max(0, min(current_health, self.max_health))
        
        # Smoothly update displayed health
        if self.displayed_health > self.health:
            self.displayed_health = max(self.health, self.displayed_health - self.health_change_speed)
        elif self.displayed_health < self.health:
            self.displayed_health = min(self.health, self.displayed_health + self.health_change_speed)
        
    def draw(self, surface):
        """Draw the health bar on the given surface."""
        # Calculate health ratio based on displayed health
        ratio = self.displayed_health / self.max_health
        
        # Draw background (empty health)
        pygame.draw.rect(surface, (255, 0, 0), (self.x, self.y, self.width, self.height))
        
        # Draw filled health
        if self.displayed_health > 0:
            pygame.draw.rect(surface, (0, 255, 0), (self.x, self.y, int(self.width * ratio), self.height))
            
            # Change color to yellow when health is low (below 30%)
            if ratio < 0.3:
                pygame.draw.rect(surface, (255, 255, 0), (self.x, self.y, int(self.width * ratio), self.height))
                
        # Draw border
        pygame.draw.rect(surface, (0, 0, 0), (self.x, self.y, self.width, self.height), 2)
        
        # Draw text showing health value
        font = pygame.font.Font(None, 24)
        text = font.render(f"{int(self.displayed_health)}/{self.max_health}", True, (255, 255, 255))
        surface.blit(text, (
            self.x + self.width // 2 - text.get_width() // 2,
            self.y + self.height // 2 - text.get_height() // 2
        ))