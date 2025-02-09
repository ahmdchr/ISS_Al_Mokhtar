import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, START_BUTTON_PATH, QUIT_BUTTON_PATH, TITLE_PATH
from map import Map

class Button:
    def __init__(self, x, y, width, height, image, hover_image):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.transform.scale(image, (width, height))
        self.hover_image = pygame.transform.scale(hover_image, (width, height))
        self.hovered = False

    def draw(self, screen):
        screen.blit(self.hover_image if self.hovered else self.image, self.rect.topleft)

    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

class MainMenu:
    def __init__(self, game_map):
        self.map = game_map
        self.title_image = pygame.transform.scale(pygame.image.load(TITLE_PATH), (627, 145))

        self.start_button = Button(
            SCREEN_WIDTH // 2 - 275, SCREEN_HEIGHT // 2, 527, 133,
            pygame.image.load(START_BUTTON_PATH), pygame.image.load(START_BUTTON_PATH)
        )
        self.quit_button = Button(
            SCREEN_WIDTH // 2 - 275, SCREEN_HEIGHT // 2 + 200, 527, 133,
            pygame.image.load(QUIT_BUTTON_PATH), pygame.image.load(QUIT_BUTTON_PATH)
        )

        self.scroll_speed = 1  # Adjust for smooth movement
        self.offset_x = 0  # Horizontal position
        self.offset_y = 0  # Vertical position
        self.direction = "right"  # Initial movement direction

        # Get the full map width and height in pixels
        self.map_width_px = self.map.visible_width * self.map.tiles[0].get_width()
        self.map_height_px = self.map.visible_height * self.map.tiles[0].get_height()

    def update(self):
        """Move in a pattern: Right → Down → Left → Up → Repeat."""
        if self.direction == "right":
            self.offset_x += self.scroll_speed
            if self.offset_x >= self.map_width_px:  # Reached the end, switch to down
                self.offset_x = self.map_width_px
                self.direction = "down"

        elif self.direction == "down":
            self.offset_y += self.scroll_speed
            if self.offset_y >= self.map_height_px:  # Reached the bottom, switch to left
                self.offset_y = self.map_height_px
                self.direction = "left"

        elif self.direction == "left":
            self.offset_x -= self.scroll_speed
            if self.offset_x <= 0:  # Reached the left, switch to up
                self.offset_x = 0
                self.direction = "up"

        elif self.direction == "up":
            self.offset_y -= self.scroll_speed
            if self.offset_y <= 0:  # Reached the top, switch to right
                self.offset_y = 0
                self.direction = "right"

    def draw(self, screen):
        """Draw the map with the updated scrolling position."""
        self.map.draw(screen, -self.offset_x, -self.offset_y)

        # Draw UI elements
        title_rect = self.title_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        screen.blit(self.title_image, title_rect)
        self.start_button.draw(screen)
        self.quit_button.draw(screen)
