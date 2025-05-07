import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, SCALED_TILE_SIZE
from Fire import Fire
from player import Player

class Knight:
    def __init__(self, x, y, run_images, idle_images, knight_id, attack_images=None):
        self.x = x
        self.y = y
        self.knight_id = knight_id
        self.speed = 10
        self.target_x = x
        self.target_y = y
        self.is_active = False

        self.run_frames = [pygame.transform.scale(pygame.image.load(p), (64, 64)) for p in run_images]
        self.idle_frames = [pygame.transform.scale(pygame.image.load(p), (64, 64)) for p in idle_images]
        self.attack_frames = [pygame.transform.scale(pygame.image.load(p), (64, 64)) for p in attack_images] if attack_images else []

        self.current_frames = self.idle_frames
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.1

        self.is_attacking = False
        self.attack_duration = 1.0  # in seconds
        self.attack_timer = 0

    def move_to(self, x, y):
        self.target_x, self.target_y = x, y
        self.is_active = True
        self.current_frames = self.run_frames

    def start_attack(self):
        if self.attack_frames:
            self.is_attacking = True
            self.attack_timer = 0
            self.current_frames = self.attack_frames
            self.current_frame = 0

    def update(self, delta_time):
        if self.is_active:
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            if abs(dx) <= self.speed and abs(dy) <= self.speed:
                self.x, self.y = self.target_x, self.target_y
                self.is_active = False
                self.start_attack()
            else:
                self.x += self.speed if dx > 0 else -self.speed
                self.y += self.speed if dy > 0 else -self.speed

        elif self.is_attacking:
            pass  # Keep attacking forever

        self.animation_timer += delta_time
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.current_frames)

    def draw(self, screen, cam_x, cam_y):
        screen.blit(self.current_frames[self.current_frame], (self.x - cam_x, self.y - cam_y))

class Cutscene:
    def __init__(self, game_map):
        self.map = game_map
        self.is_playing = False
        self.step_timer = 0
        self.camera_x = 0
        self.camera_y = 0
        self.camera_target_x = 0
        self.camera_target_y = 0
        self.camera_speed = 3
        

        self.map_width = self.map.visible_width * SCALED_TILE_SIZE
        self.map_height = self.map.visible_height * SCALED_TILE_SIZE

        self.knight_run = [
            'knight_run/knight_run_left/knight_run_left_1.png',
            'knight_run/knight_run_left/knight_run_left_2.png',
            'knight_run/knight_run_left/knight_run_left_3.png',
            'knight_run/knight_run_left/knight_run_left_4.png'
        ]
        self.knight_idle = [
            'knight_idle/knight_idle_left/knight_idle_left_1.png',
            'knight_idle/knight_idle_left/knight_idle_left_2.png',
            'knight_idle/knight_idle_left/knight_idle_left_3.png'
        ]
        self.knight_attack = [
            'knight_attack/knight_attack_left/knight_attack_left_1.png',
            'knight_attack/knight_attack_left/knight_attack_left_2.png',
            'knight_attack/knight_attack_left/knight_attack_left_3.png'
        ]

        self.knights = [
            Knight(self.map_width - 100, 100 + i * 20, self.knight_run, self.knight_idle, i, self.knight_attack)
            for i in range(6)
        ]

        self.fires = []
        self.fire_locations = [
            (self.map_width - 1020, 250),
            (self.map_width - 720, 650),
            (self.map_width - 720, 250)
        ]
        self.large_fire_locations = [
            (self.map_width - 980, 200),
            (self.map_width - 680, 600),
            (self.map_width - 680, 200)
        ]

        self.steps = []
        self.current_step = 0
        self.cutscene_duration = 15.0

        self.player = Player(game_map)


    def start(self):
        self.is_playing = True
        self.step_timer = 0
        self.camera_x = self.map_width - 100
        self.camera_y = 100
        self.current_step = 0
        self.player.x = 352
        self.player.y = 290
        self.player.direction = "left"
        self.player.attacking = True

        self.steps = [
            (0.5, self.move_knight, (0, self.map_width - 1000, 250)),
            (1.0, self.move_knight, (1, self.map_width - 700, 650)),
            (1.5, self.move_knight, (2, self.map_width - 700, 250)),
            (2.0, self.set_camera_position, (self.map_width - 1500, 0, False)),
            (3.0, self.check_and_create_fires, ()),
            (3.5, self.check_and_create_large_fires, ()),
            (4.0, self.set_camera_position, (0,0,True)),
            (8.5, self.end_cutscene, ())
        ]

    def move_knight(self, knight_id, x, y):
        if 0 <= knight_id < len(self.knights):
            self.knights[knight_id].move_to(x, y)

    def set_camera_position(self, x, y, accel):
        if accel:
            self.camera_speed = 13
        else: 
            self.camera_speed = 3
        self.camera_target_x = x
        self.camera_target_y = y
        self.clamp_camera()

    def clamp_camera(self):
        self.camera_x = max(0, min(self.camera_x, self.map_width - SCREEN_WIDTH))
        self.camera_y = max(0, min(self.camera_y, self.map_height - SCREEN_HEIGHT))

    def check_and_create_fires(self):
        for i, (fx, fy) in enumerate(self.fire_locations):
            if self.knight_arrived(i):
                if not any(abs(f.x - fx) < 10 and abs(f.y - fy) < 10 for f in self.fires):
                    self.fires.append(Fire(fx, fy, scale=1.25))

    def check_and_create_large_fires(self):
        for i, (fx, fy) in enumerate(self.large_fire_locations):
            if self.knight_arrived(i):
                if not any(abs(f.x - fx) < 10 and abs(f.y - fy) < 10 and f.scale > 2.0 for f in self.fires):
                    self.fires.append(Fire(fx, fy, scale=3.0))

    def knight_arrived(self, idx):
        return not self.knights[idx].is_active

    def all_knights_arrived(self):
        return all(not k.is_active and not k.is_attacking for k in self.knights)

    def update(self, delta_time):
        if not self.is_playing:
            return False

        self.step_timer += delta_time

        while self.current_step < len(self.steps) and self.step_timer >= self.steps[self.current_step][0]:
            _, func, args = self.steps[self.current_step]
            func(*args)
            self.current_step += 1

        for knight in self.knights:
            knight.update(delta_time)

        for fire in self.fires:
            fire.update(delta_time)

        # Smooth camera movement
        if self.camera_x < self.camera_target_x:
            self.camera_x += min(self.camera_speed, self.camera_target_x - self.camera_x)
        elif self.camera_x > self.camera_target_x:
            self.camera_x -= min(self.camera_speed, self.camera_x - self.camera_target_x)

        if self.camera_y < self.camera_target_y:
            self.camera_y += min(self.camera_speed, self.camera_target_y - self.camera_y)
        elif self.camera_y > self.camera_target_y:
            self.camera_y -= min(self.camera_speed, self.camera_y - self.camera_target_y)

        self.clamp_camera()

        if self.all_knights_arrived() and self.current_step >= len(self.steps) and self.step_timer >= self.cutscene_duration:
            self.is_playing = False

        return self.is_playing

    def end_cutscene(self):
        self.is_playing = False

    def draw(self, screen, deltatime):
        self.map.draw(screen, self.camera_x, self.camera_y)
        for fire in self.fires:
            fire.draw(screen, self.camera_x, self.camera_y)
        for knight in self.knights:
            knight.draw(screen, self.camera_x, self.camera_y)
        self.player.update(deltatime, pygame.key.get_pressed())
        self.player.draw(screen)

