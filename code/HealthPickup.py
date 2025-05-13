import pygame

class HealthPickup(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path, heal_amount=20, scale=2.0):
        super().__init__()
        original_image = pygame.image.load(image_path).convert_alpha()  # Keeps transparency
        width = int(original_image.get_width() * scale)
        height = int(original_image.get_height() * scale)
        self.image = pygame.transform.scale(original_image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.heal_amount = heal_amount

    def draw(self, screen, camera_x=0, camera_y=0):
        screen.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))
