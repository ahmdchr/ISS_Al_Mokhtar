### Refactored KnightEnemy.py (Fixed load_images type error)
# Simplified patrol, animation, and attack logic for better clarity and performance

import pygame
import math
from enemy_bot import Enemy
from HealthBar import HealthBar

class KnightEnemy(Enemy):
    def __init__(self, x, y, knight_id):
        super().__init__()  # Placeholder for parent

        self.knight_id = knight_id
        self.rect = pygame.Rect(x, y, 64, 64)

        self.damage_sound = pygame.mixer.Sound("damage.mp3")
        self.damage_sound.set_volume(0.5)  # optional: adjust volume

        self.attack_radius = 100
        self.patrol_radius = 250
        self.patrol_points = self.generate_patrol_points(x, y)
        self.current_patrol_index = 0
        self.set_target_to_current_patrol()

        self.movement_speed = 3
        self.health = 100
        self.dead = False

        self.update_time = pygame.time.get_ticks()
        self.frame_index = 0
        self.action = 0
        self.attack_cooldown = 0
        self.attack_cooldown_max = 60
        self.attacking = False
        self.Flip = False

        self.idle_frames = self.load_images('knight_idle/knight_idle_left', 3)
        self.run_frames = self.load_images('knight_run/knight_run_left', 4)
        self.attack_frames = self.load_images('knight_attack/knight_attack_left', 4)
        self.death_frames = [pygame.transform.scale(pygame.image.load("knight_dead_animation.png"), (64, 64))]

        self.animation_list = [self.idle_frames, self.run_frames, self.attack_frames, self.death_frames]
        self.image = self.idle_frames[0]

        self.health_bar = HealthBar(self.rect.x, self.rect.y - 20, self.health, self.health)

    def load_images(self, folder, count):
        if isinstance(count, list):
            count = len(count)  # Convert list to its length if needed
        return [
            pygame.transform.scale(pygame.image.load(f"{folder}/{folder.split('/')[-1]}_{i+1}.png"), (64, 64))
            for i in range(int(count))
        ]

    def generate_patrol_points(self, x, y):
        return [(x, y), (x + self.patrol_radius, y), (x + self.patrol_radius, y + self.patrol_radius), (x, y + self.patrol_radius)]

    def set_target_to_current_patrol(self):
        self.target_x, self.target_y = self.patrol_points[self.current_patrol_index]

    def move_to_next_patrol_point(self):
        self.current_patrol_index = (self.current_patrol_index + 1) % len(self.patrol_points)
        self.set_target_to_current_patrol()

    def update(self, delta_time, player):
        self.health_bar.x = self.rect.x
        self.health_bar.y = self.rect.y - 20
        self.health_bar.update(self.health)

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        if self.health <= 0:
            self.dead = True

        if self.dead:
            self.update_action(3)
            self.image = self.death_frames[0]  # Show grave image only
            return

        # Get distance from player
        distance = math.hypot(player.rect.centerx - self.rect.centerx, player.rect.centery - self.rect.centery)

        if distance <= 100 and not player.dead:
            self.face_target(player)
            self.move_towards(player.rect.centerx, player.rect.centery)
            self.update_action(1)

            if distance <= 50 and self.attack_cooldown == 0:
                self.attacking = True
                self.update_action(2)
                self.attack(player)
                self.attack_cooldown = self.attack_cooldown_max
        else:
            # Patrol only if not in 50-radius range
            if self.is_at_target():
                self.move_to_next_patrol_point()
            self.move_towards(self.target_x, self.target_y)
            self.update_action(1 if not self.is_at_target() else 0)

        self.animate()


    def face_target(self, target):
        self.Flip = target.rect.centerx < self.rect.centerx

    def is_at_target(self):
        return abs(self.rect.x - self.target_x) < 10 and abs(self.rect.y - self.target_y) < 10

    def move_towards(self, x, y):
        dx, dy = x - self.rect.centerx, y - self.rect.centery
        dist = max(1, math.hypot(dx, dy))
        dx, dy = dx / dist * self.movement_speed, dy / dist * self.movement_speed
        self.rect.x += dx
        self.rect.y += dy

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def animate(self):
        now = pygame.time.get_ticks()
        cooldown = 100
        if now - self.update_time > cooldown:
            self.update_time = now
            self.frame_index = (self.frame_index + 1) % len(self.animation_list[self.action])
        self.image = self.animation_list[self.action][self.frame_index]

    def attack(self, player):
        offset = -40 if self.Flip else self.rect.width
        attack_rect = pygame.Rect(self.rect.x + offset, self.rect.y, 40, self.rect.height)
        if attack_rect.colliderect(player.rect):
            self.damage_sound.play()
            player.health -= 5

    def draw(self, surface, camera_x=0, camera_y=0):
        img = pygame.transform.flip(self.image, self.Flip, False)
        surface.blit(img, (self.rect.x - camera_x, self.rect.y - camera_y))
        
        if not self.dead:
            self.health_bar.draw(surface, camera_x, camera_y)