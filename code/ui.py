import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, START_BUTTON_PATH, QUIT_BUTTON_PATH, TITLE_PATH
from map import Map

class Button:
    """A class to create buttons with hover effects."""
    def __init__(self, x, y, width, height, image_path):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.transform.scale(pygame.image.load(image_path), (width, height))
        self.hover_image = self.image.copy()  # Same image for now, can be customized
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

class MainMenu:
    """The main menu of the game with a scrolling background map."""
    def __init__(self, game_map):
        self.map = game_map
        self.title_image = pygame.transform.scale(pygame.image.load(TITLE_PATH), (627, 145))

        # Create Start and Quit buttons
        self.start_button = Button(
            SCREEN_WIDTH // 2 - 275, SCREEN_HEIGHT // 2, 527, 133, START_BUTTON_PATH
        )
        self.quit_button = Button(
            SCREEN_WIDTH // 2 - 275, SCREEN_HEIGHT // 2 + 200, 527, 133, QUIT_BUTTON_PATH
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
        self.map.draw(screen, -self.offset_x, -self.offset_y)  # Draw the map with offset

        # Draw the title
        title_rect = self.title_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        screen.blit(self.title_image, title_rect)
        
        # Draw the buttons
        self.start_button.draw(screen)
        self.quit_button.draw(screen)