import pygame
from settings import PLAYER_SPEED, ANIMATION_SPEED

class Character:
    def __init__(self, game_map):
        self.x, self.y = 600, 300
        self.direction = 0  # 0: down, 1: left, 2: right, 3: up
        self.current_frame = 0
        self.animation_timer = 0
        self.speed = PLAYER_SPEED
        self.animation_speed = ANIMATION_SPEED
        self.map = game_map
        self.facing = "down"

        self.image_idle = self.load_all_images('idle_animation_amira', 3)
        self.image_run = self.load_all_images('run_animation_amira', 4)

        self.is_moving = False  # track movement

    def load_all_images(self, action, frames, size=(64, 64)):
        return {
            'down': [pygame.transform.scale(pygame.image.load(f'{action}/amira_down/amira_down_{i+1}.png'), size) for i in range(frames)],
            'right': [pygame.transform.scale(pygame.image.load(f'{action}/amira_right/amira_right_{i+1}.png'), size) for i in range(frames)],
            'left': [pygame.transform.scale(pygame.image.load(f'{action}/amira_left/amira_left_{i+1}.png'), size) for i in range(frames)],
            'up': [pygame.transform.scale(pygame.image.load(f'{action}/amira_up/amira_up_{i+1}.png'), size) for i in range(frames)]
        }

    def draw(self, screen):
        directions = ['down', 'left', 'right', 'up']
        direction = directions[self.direction]

        self.animation_timer += 1
        if self.animation_timer >= (1 / self.animation_speed) * 60:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % 4

        if self.is_moving:
            frame = self.current_frame % 4
            screen.blit(self.image_run[direction][frame], (self.x, self.y))
        else:
            frame = self.current_frame % 3
            screen.blit(self.image_idle[direction][frame], (self.x, self.y))

    def update(self, target_x, target_y):
        self.is_moving = False

        dx = target_x - self.x
        dy = target_y - self.y

        if abs(dx) > 2:
            if dx > 0:
                self.x += self.speed * 0.05
                self.direction = 2  # right
            else:
                self.x -= self.speed * 0.05
                self.direction = 1  # left
            self.is_moving = True

        if abs(dy) > 2:
            if dy > 0:
                self.y += self.speed * 0.05
                self.direction = 0  # down
            else:
                self.y -= self.speed * 0.05
                self.direction = 3  # up
            self.is_moving = True
