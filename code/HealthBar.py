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
        
    def draw(self, surface, camera_x=0, camera_y=0):
        """Draw the health bar on the given surface, adjusted by camera offset."""
        ratio = self.displayed_health / self.max_health

        draw_x = self.x - camera_x
        draw_y = self.y - camera_y

        pygame.draw.rect(surface, (255, 0, 0), (draw_x, draw_y, self.width, self.height))

        if self.displayed_health > 0:
            fill_color = (255, 255, 0) if ratio < 0.3 else (0, 255, 0)
            pygame.draw.rect(surface, fill_color, (draw_x, draw_y, int(self.width * ratio), self.height))

        pygame.draw.rect(surface, (0, 0, 0), (draw_x, draw_y, self.width, self.height), 2)

        font = pygame.font.Font(None, 24)
        text = font.render(f"{int(self.displayed_health)}/{self.max_health}", True, (255, 255, 255))
        surface.blit(text, (
            draw_x + self.width // 2 - text.get_width() // 2,
            draw_y + self.height // 2 - text.get_height() // 2
        ))

