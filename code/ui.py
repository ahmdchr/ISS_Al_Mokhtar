import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, START_BUTTON_PATH, QUIT_BUTTON_PATH, TITLE_PATH, START_BUTTON_HOVER_PATH, QUIT_BUTTON_HOVER_PATH
from map import Map

class Button:
    """A class to create buttons with hover effects."""
    def __init__(self, x, y, width, height, image_path, hover_image_path):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.transform.scale(pygame.image.load(image_path), (width, height))
        self.hover_image = pygame.transform.scale(pygame.image.load(hover_image_path), (width, height))
        self.hovered = False

    def draw(self, screen):
        """Draw the button with hover effect."""
        if self.hovered:
            screen.blit(self.hover_image, self.rect.topleft)
        else:
            screen.blit(self.image, self.rect.topleft)

    def check_hover(self, mouse_pos):
        """Check if the mouse is hovering over the button."""
        self.hovered = self.rect.collidepoint(mouse_pos)

class HealthBar:
    """Displays hearts as a health bar in the top right corner."""
    def __init__(self, max_health, heart_image_path):
        self.max_health = max_health
        self.current_health = max_health
        self.heart_image = pygame.image.load(heart_image_path)
        self.heart_image = pygame.transform.scale(self.heart_image, (48, 69))  # Adjust heart size

    def draw(self, screen):
        """Draws the heart-based health bar."""
        x_offset = SCREEN_WIDTH - (self.current_health * 50) - 10  # Align to top-right
        y_offset = 10  # Small margin from the top

        for i in range(self.current_health):
            screen.blit(self.heart_image, (x_offset + i * 50, y_offset))  # Space out hearts

    def update_health(self, new_health):
        """Updates the displayed health value."""
        self.current_health = max(0, min(new_health, self.max_health))  # Keep health within range

class MainMenu:
    """The main menu of the game with a scrolling background map."""
    def __init__(self, game_map):
        self.map = game_map
        self.title_image = pygame.transform.scale(pygame.image.load(TITLE_PATH), (627, 145))

        # Create Start and Quit buttons
        self.start_button = Button(
            SCREEN_WIDTH // 2 - 275, SCREEN_HEIGHT // 2, 527, 133, START_BUTTON_PATH, START_BUTTON_HOVER_PATH
        )
        self.quit_button = Button(
            SCREEN_WIDTH // 2 - 275, SCREEN_HEIGHT // 2 + 200, 527, 133, QUIT_BUTTON_PATH, QUIT_BUTTON_HOVER_PATH
        )

        # Scrolling background settings
        self.scroll_speed = 1  # Speed of the scrolling effect
        self.offset_x = 0  # Horizontal scrolling position
        self.offset_y = 0  # Vertical scrolling position
        self.direction = "right"  # Initial movement direction

        # Get the total width and height of the map in pixels
        self.map_width_px = self.map.visible_width * self.map.tiles[0].get_width()
        self.map_height_px = self.map.visible_height * self.map.tiles[0].get_height()

    def update(self):
        """Update the scrolling background movement."""
        if self.direction == "right":
            self.offset_x += self.scroll_speed
            if self.offset_x >= self.map_width_px:  # Reached the right end
                self.offset_x = self.map_width_px
                self.direction = "down"

        elif self.direction == "down":
            self.offset_y += self.scroll_speed
            if self.offset_y >= self.map_height_px:  # Reached the bottom
                self.offset_y = self.map_height_px
                self.direction = "left"

        elif self.direction == "left":
            self.offset_x -= self.scroll_speed
            if self.offset_x <= 0:  # Reached the left end
                self.offset_x = 0
                self.direction = "up"

        elif self.direction == "up":
            self.offset_y -= self.scroll_speed
            if self.offset_y <= 0:  # Reached the top
                self.offset_y = 0
                self.direction = "right"

    def draw(self, screen):
        """Draw the menu, including the scrolling background and buttons."""
        self.map.draw(screen, self.offset_x, self.offset_y)  # Draw the map with offset

        # Draw the title
        title_rect = self.title_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        screen.blit(self.title_image, title_rect)
        
        # Draw the buttons
        self.start_button.draw(screen)
        self.quit_button.draw(screen)
