### Refactored enemy_bot.py (Fixed animation index error)
# Adds safety for empty animation lists and fallback behavior

import pygame
import math

class Enemy():
    def __init__(self, x, y, flip, data, sprite_sheet, animation_steps):
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.rect = pygame.Rect(x, y, 80, 180)
        self.update_time = pygame.time.get_ticks()
        self.Flip = flip
        self.action = 0
        self.frame_index = 0
        self.animation_list = self.load_images(sprite_sheet, animation_steps)

        if self.animation_list and self.animation_list[0]:
            self.image = self.animation_list[self.action][self.frame_index]
        else:
            self.image = pygame.Surface((64, 64))  # fallback placeholder

        self.attack_move = 0
        self.running = False
        self.moving_up = False
        self.moving_down = False
        self.moving_right = False
        self.moving_left = False
        self.dead = False
        self.health = 100

    def load_images(self, images_sheet, animation_steps):
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_image = images_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(pygame.transform.scale(temp_image, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list

    def get_target_status(self, target):
        if not self.dead and abs(self.rect.x - target.rect.x) <= 100:
            self.attack_move = True
        self.Flip = target.rect.x < self.rect.x

    def update(self, screen, target):
        animation_cooldown = 300

        if self.attack_move and target.attacking:
            self.update_action(4)
            self.attack(screen, target)
        if self.dead:
            self.update_action(6)
            self.image = self.animation_list[6][-1] if self.animation_list[6] else pygame.Surface((64, 64))
        else:
            if target.dead:
                self.image = self.animation_list[self.action][1] if self.animation_list[self.action] else pygame.Surface((64, 64))
            else:
                if self.animation_list[self.action]:
                    self.image = self.animation_list[self.action][self.frame_index]

        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
            if self.animation_list[self.action]:
                self.frame_index %= len(self.animation_list[self.action])
            else:
                self.frame_index = 0

    def move(self, target):
        SPEED = 3
        dx = target.rect.x - self.rect.x
        dy = target.rect.y - self.rect.y
        distance = math.hypot(dx, dy)
        if distance > 93:
            self.rect.x += dx / distance * SPEED
            self.rect.y += dy / distance * SPEED

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        pygame.draw.rect(surface, (0, 100, 100), self.rect)
        img = pygame.transform.flip(self.image, self.Flip, False)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))

    def attack(self, surface, target):
        if self.Flip:
            attack_rect = pygame.Rect(self.rect.centerx - 110, self.rect.y + 30, self.rect.width - 10, self.rect.height - 30)
        else:
            attack_rect = pygame.Rect(self.rect.centerx + 40, self.rect.y + 30, self.rect.width - 10, self.rect.height - 30)

        if attack_rect.colliderect(target.rect):
            target.health -= 10
