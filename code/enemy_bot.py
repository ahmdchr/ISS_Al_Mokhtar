import pygame
import math
from HealthBar import HealthBar

class Enemy:
    def __init__(self):
        self.x, self.y = 700, 400
        self.rect = pygame.Rect(self.x, self.y, 80, 180)
        self.speed = 3.5
        self.facing = "left"
        self.id = id

        # Animation
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.15
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()


        self.damage_sound = pygame.mixer.Sound("damage.mp3")
        self.damage_sound.set_volume(0.5)  # optional: adjust volume

        # Combat
        self.attack_move = False
        self.damage_applied = False
        self.dead = False
        self.health = 100
        self.max_health = 100
        self.health_bar = HealthBar(self.x, self.y - 30, self.health, self.max_health)
        self.flip = False
        self.running = False

        # Load animations
        self.image_idle = self.load_all_images('idle_animation_boss', 3)
        self.image_run = self.load_all_images('run_animation_boss', 4)
        self.image_attack = self.load_all_images('attack_animation_boss', 4)
        self.image_death = [pygame.transform.scale(pygame.image.load("knight_dead_animation.png"), (64, 64))]

    def load_all_images(self, action, frames, size=(120, 120)):
        return {
            'down': [pygame.transform.scale(pygame.image.load(f'{action}/boss_down/boss_down_{i+1}.png'), size) for i in range(frames)],
            'left': [pygame.transform.scale(pygame.image.load(f'{action}/boss_left/boss_left_{i+1}.png'), size) for i in range(frames)],
            'right': [pygame.transform.scale(pygame.image.load(f'{action}/boss_right/boss_right_{i+1}.png'), size) for i in range(frames)],
            'up': [pygame.transform.scale(pygame.image.load(f'{action}/boss_up/boss_up_{i+1}.png'), size) for i in range(frames)]
        }

    def update(self, screen, target):
        self.health_bar.update(self.health)

        if self.health <= 0 and not self.dead:
            self.dead = True
            self.current_frame = 0
            self.attack_move = False
            self.running = False

        if not self.dead:
            self.get_target_status(target)

        # Animation frame update
        self.animation_timer += self.animation_speed
        if self.animation_timer >= 1:
            current_animation = self.get_current_animation()
            if current_animation:
                if self.dead and self.current_frame < len(current_animation) - 1:
                    self.current_frame += 1
                elif not self.dead:
                    self.current_frame = (self.current_frame + 1) % len(current_animation)
            self.animation_timer = 0

        if self.attack_move and self.current_frame == 0:
            self.damage_applied = False

        if self.attack_move and not self.dead:
            self.attack(screen, target)

    def get_current_animation(self):
        if self.dead:
            return self.image_death
        elif self.attack_move:
            return self.image_attack.get(self.facing, [])
        elif self.running:
            return self.image_run.get(self.facing, [])
        return self.image_idle.get(self.facing, [])

    def get_target_status(self, target):
        if self.dead:
            return

        dx = target.rect.centerx - self.rect.centerx
        dy = target.rect.centery - self.rect.centery

        if target.rect.x < self.rect.x:
            self.facing = "left"
            target.direction = "right"
        else:
            self.facing = "right"
            target.direction = "left"

        if target.rect.y < self.rect.y - 30:
            self.facing = "up"
            target.direction = "down"
        elif target.rect.y > self.rect.y + 80:
            self.facing = "down"
            target.direction = "up"

        if dx >= 20 and abs(dy) <= 50:
            self.attack_move = True
            self.running = False
            self.facing = "right"
        elif dx <= -20 and abs(dy) <= 50:
            self.attack_move = True
            self.running = False
            self.facing = "left"
        elif dy <= -20 and abs(dx) <= 50:
            self.attack_move = True
            self.running = False
            self.facing = "up"
        elif dy >= 20 and abs(dx) <= 50:
            self.attack_move = True
            self.running = False
            self.facing = "down"
        else:
            self.attack_move = False
            self.running = abs(dx) > 93 or abs(dy) > 93

    def move(self, target):
        if self.dead:
            return

        dx = target.rect.x - self.rect.x - 15
        dy = target.rect.y - self.rect.y
        distance = math.sqrt(dx**2 + dy**2)

        if distance > 93:
            dx /= distance
            dy /= distance
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed
            self.x, self.y = self.rect.x, self.rect.y
            self.running = True
        else:
            self.running = False

    def attack(self, surface, target):
        if not self.attack_move:
            return

        attack_rect = None

        if self.facing == "left":
            attack_rect = pygame.Rect(self.rect.centerx - 60, self.rect.y, self.rect.width - 20, self.rect.height - 120)
        elif self.facing == "right":
            attack_rect = pygame.Rect(self.rect.centerx + 10, self.rect.y, self.rect.width - 15, self.rect.height - 120)
        elif self.facing == "up":
            attack_rect = pygame.Rect(self.rect.centerx - 25, self.rect.y - 50, self.rect.width, 70)
        elif self.facing == "down":
            attack_rect = pygame.Rect(self.rect.centerx - 30, self.rect.bottom - 80, self.rect.width, 70)

        if self.attack_move:
            # pygame.draw.rect(surface, (255, 255, 0), attack_rect, 2)  # Debug
            current_animation = self.get_current_animation()
            if current_animation and len(current_animation) > 0:
                if self.current_frame == 2 and not self.damage_applied and attack_rect.colliderect(target.rect):
                    self.damage_sound.play()
                    target.health -= 10
                    self.damage_applied = True

    def draw(self, surface, camera_x=0, camera_y=0):
        self.health_bar.x = self.rect.centerx - self.health_bar.width // 2
        self.health_bar.y = self.rect.top - 25
        self.health_bar.draw(surface)

        draw_x = self.x - camera_x
        draw_y = self.y - camera_y

        frames = self.get_current_animation()
        if not frames or len(frames) == 0:
            return

        frame = frames[min(self.current_frame, len(frames) - 1)]

        if self.flip:
            frame = pygame.transform.flip(frame, True, False)

        surface.blit(frame, (draw_x, draw_y))
