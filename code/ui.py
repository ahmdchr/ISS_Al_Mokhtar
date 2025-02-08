import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_PATH, START_BUTTON_PATH, QUIT_BUTTON_PATH, TITLE_PATH

class Button:
    def __init__(self, x, y, width, height, image, hover_image):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.transform.scale(image, (width, height))
        self.hover_image = pygame.transform.scale(hover_image, (width, height))
        self.hovered = False

    def draw(self, screen):
        if self.hovered:
            screen.blit(self.hover_image, self.rect.topleft)
        else:
            screen.blit(self.image, self.rect.topleft)

    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

class MainMenu:
    def __init__(self):
        self.background = pygame.transform.scale(pygame.image.load(BACKGROUND_PATH), (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.title_image = pygame.transform.scale(pygame.image.load(TITLE_PATH), (627, 145))

        self.start_button = Button(
            SCREEN_WIDTH // 2 - 275, SCREEN_HEIGHT // 2, 527, 133,
            pygame.image.load(START_BUTTON_PATH), pygame.image.load(START_BUTTON_PATH)
        )
        self.quit_button = Button(
            SCREEN_WIDTH // 2 - 275, SCREEN_HEIGHT // 2 + 200, 527, 133,
            pygame.image.load(QUIT_BUTTON_PATH), pygame.image.load(QUIT_BUTTON_PATH)
        )

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        title_rect = self.title_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        screen.blit(self.title_image, title_rect)
        self.start_button.draw(screen)
        self.quit_button.draw(screen)