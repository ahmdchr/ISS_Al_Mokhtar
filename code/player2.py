import pygame
from settings import PLAYER_SPEED, ANIMATION_SPEED, SCALED_TILE_SIZE

class Player2:
    def __init__(self, game_map):
        self.x, self.y = 300, 450
        self.direction = 'down'
        self.facing = self.direction
        self.current_frame = 0
        self.animation_timer = 0
        self.speed = PLAYER_SPEED
        self.animation_speed = ANIMATION_SPEED
        self.map = game_map  # unused but left intact

        self.attacking = False
        self.attack_duration = 0.4
        self.attack_timer = 0

        self.health = 100
        self.max_health = 100
        self.dead = False

        self.rect = pygame.Rect(self.x, self.y, 64, 64)

        self.image_idle = self.load_all_images('idle_animation', 3)
        self.image_run = self.load_all_images('run_animation', 4)
        self.image_attack = self.load_all_images('attack_animation', 4)

    def load_all_images(self, action, frames, size=(64, 64)):
        return {
            'down': [pygame.transform.scale(pygame.image.load(f'{action}/hero_down/hero_down_{i+1}.png'), size) for i in range(frames)],
            'left': [pygame.transform.scale(pygame.image.load(f'{action}/hero_left/hero_left_{i+1}.png'), size) for i in range(frames)],
            'right': [pygame.transform.scale(pygame.image.load(f'{action}/hero_right/hero_right_{i+1}.png'), size) for i in range(frames)],
            'up': [pygame.transform.scale(pygame.image.load(f'{action}/hero_up/hero_up_{i+1}.png'), size) for i in range(frames)]
        }

    # def can_move(self, new_x, new_y):
    #     tile_x = int(new_x // SCALED_TILE_SIZE)
    #     tile_y = int(new_y // SCALED_TILE_SIZE)
    #     return not self.map.is_obstacle(tile_x, tile_y)

    def update(self, delta_time, keys):
        if self.health <= 0:
            self.dead = True
            return

        new_x, new_y = self.x, self.y
        moved = False

        if self.attacking:
            self.attack_timer -= delta_time
            if self.attack_timer <= 0:
                self.attacking = False

        directions = {
            pygame.K_LEFT: ('left', -self.speed * delta_time, 0),
            pygame.K_q:    ('left', -self.speed * delta_time, 0),
            pygame.K_RIGHT:('right', self.speed * delta_time, 0),
            pygame.K_d:    ('right', self.speed * delta_time, 0),
            pygame.K_UP:   ('up', 0, -self.speed * delta_time),
            pygame.K_z:    ('up', 0, -self.speed * delta_time),
            pygame.K_DOWN: ('down', 0, self.speed * delta_time),
            pygame.K_s:    ('down', 0, self.speed * delta_time)
        }

        for key, (dir_str, dx, dy) in directions.items():
            if keys[key]:
                self.direction = dir_str
                new_x += dx
                new_y += dy
                moved = True

        if moved:
            self.x, self.y = new_x, new_y

            # Limit horizontal movement within screen bounds
            self.x = max(0, min(self.x, pygame.display.get_surface().get_width() - self.rect.width))
            
            # Limit vertical movement, accounting for top UI margin
            self.y = max(45, min(self.y, pygame.display.get_surface().get_height() - self.rect.height))

            self.rect.topleft = (int(self.x), int(self.y))

        self.animation_timer += delta_time
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % 4

    def attack_check(self, screen, enemy):
        offset = 40
        attack_rects = {
            'down': pygame.Rect(self.x, self.y + offset, 64, 50),
            'left': pygame.Rect(self.x - offset, self.y, 50, 64),
            'right': pygame.Rect(self.x + offset, self.y, 50, 64),
            'up': pygame.Rect(self.x, self.y - offset, 64, 50)
        }

        attack_rect = attack_rects[self.direction]

        # pygame.draw.rect(screen, (0,255,255), attack_rect)

        if attack_rect.colliderect(enemy.rect) and not enemy.dead:
            enemy.health -= 10
            if enemy.health <= 0:
                enemy.dead = True

    def draw(self, screen):
        # cam_x, cam_y = self.map.camera_x, self.map.camera_y  # disabled camera
        cam_x, cam_y = 0, 0  # draw relative to screen

        if self.dead:
            dead_img = pygame.image.load('mokhtar_dead_animation.png')
            big_dead_img = pygame.transform.scale(dead_img, (dead_img.get_width() * 5, dead_img.get_height() * 5))
            screen.blit(big_dead_img, (self.x - cam_x, self.y - cam_y))
            return

        if self.attacking:
            img = self.image_attack[self.direction][self.current_frame]
        else:
            keys = pygame.key.get_pressed()
            if any(keys[k] for k in [pygame.K_LEFT, pygame.K_q, pygame.K_RIGHT, pygame.K_d, pygame.K_UP, pygame.K_z, pygame.K_DOWN, pygame.K_s]):
                img = self.image_run[self.direction][self.current_frame]
            else:
                img = self.image_idle[self.direction][self.current_frame % 3]

        screen.blit(img, (self.x - cam_x, self.y - cam_y))
        # pygame.draw.rect(screen, (255, 0, 0), (self.rect.x - cam_x, self.rect.y - cam_y, self.rect.width, self.rect.height), 1)
