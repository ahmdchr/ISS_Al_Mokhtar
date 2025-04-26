### Refactored ui.py
# Clean main menu logic, modular buttons, and health bar animations

import pygame
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    START_BUTTON_PATH, QUIT_BUTTON_PATH,
    START_BUTTON_HOVER_PATH, QUIT_BUTTON_HOVER_PATH,
    TITLE_PATH
)

class Button:
    def __init__(self, x, y, width, height, image_path, hover_path):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.transform.scale(pygame.image.load(image_path), (width, height))
        self.hover_image = pygame.transform.scale(pygame.image.load(hover_path), (width, height))
        self.hovered = False

    def draw(self, screen):
        screen.blit(self.hover_image if self.hovered else self.image, self.rect.topleft)

    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

class HealthBar:
    def __init__(self, x, y, health, max_health):
        self.x, self.y = x, y
        self.health = health
        self.max_health = max_health
        self.displayed_health = health
        self.width, self.height = 200, 20
        self.change_speed = 3

    def update(self, new_health):
        self.health = max(0, min(new_health, self.max_health))
        if self.displayed_health > self.health:
            self.displayed_health = max(self.health, self.displayed_health - self.change_speed)
        elif self.displayed_health < self.health:
            self.displayed_health = min(self.health, self.displayed_health + self.change_speed)

    def draw(self, surface):
        ratio = self.displayed_health / self.max_health
        pygame.draw.rect(surface, (255, 0, 0), (self.x, self.y, self.width, self.height))

        if self.displayed_health > 0:
            fill_color = (255, 255, 0) if ratio < 0.3 else (0, 255, 0)
            pygame.draw.rect(surface, fill_color, (self.x, self.y, int(self.width * ratio), self.height))

        pygame.draw.rect(surface, (0, 0, 0), (self.x, self.y, self.width, self.height), 2)
        font = pygame.font.Font(None, 24)
        text = font.render(f"{int(self.displayed_health)}/{self.max_health}", True, (255, 255, 255))
        surface.blit(text, (
            self.x + self.width // 2 - text.get_width() // 2,
            self.y + self.height // 2 - text.get_height() // 2
        ))

class MainMenu:
    def __init__(self, game_map):
        self.map = game_map
        self.title_image = pygame.transform.scale(pygame.image.load(TITLE_PATH), (627, 145))
        self.start_button = Button(SCREEN_WIDTH//2 - 275, SCREEN_HEIGHT//2, 527, 133, START_BUTTON_PATH, START_BUTTON_HOVER_PATH)
        self.quit_button = Button(SCREEN_WIDTH//2 - 275, SCREEN_HEIGHT//2 + 200, 527, 133, QUIT_BUTTON_PATH, QUIT_BUTTON_HOVER_PATH)

        self.scroll_speed = 1
        self.offset_x = 0
        self.offset_y = 0
        self.direction = "right"
        tile_width = self.map.tiles[0].get_width()
        tile_height = self.map.tiles[0].get_height()
        self.map_width_px = self.map.visible_width * tile_width
        self.map_height_px = self.map.visible_height * tile_height

    def update(self):
        if self.direction == "right":
            self.offset_x += self.scroll_speed
            if self.offset_x >= self.map_width_px:
                self.offset_x = self.map_width_px
                self.direction = "down"
        elif self.direction == "down":
            self.offset_y += self.scroll_speed
            if self.offset_y >= self.map_height_px:
                self.offset_y = self.map_height_px
                self.direction = "left"
        elif self.direction == "left":
            self.offset_x -= self.scroll_speed
            if self.offset_x <= 0:
                self.offset_x = 0
                self.direction = "up"
        elif self.direction == "up":
            self.offset_y -= self.scroll_speed
            if self.offset_y <= 0:
                self.offset_y = 0
                self.direction = "right"

    def draw(self, screen):
        self.map.draw(screen, self.offset_x, self.offset_y)
        title_rect = self.title_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        screen.blit(self.title_image, title_rect)
        self.start_button.draw(screen)
        self.quit_button.draw(screen)
