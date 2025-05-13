import pygame, random
from player2 import Player2
from enemy_bot import Enemy
from map import Map
from settings import SCREEN_WIDTH, WHITE, SCREEN_HEIGHT
from UIOverlay import UIOverlay

class BossFightScene:
    def __init__(self, screen, health):
        self.screen = screen
        self.fighter = Player2(Map(True))
        self.fighter.health = health
        self.enemy = Enemy()
        self.enemies_left = 1
        self.enemies_killed = 6
        self.victory = False
        self.victory_start_time = 0
        self.game_over = False
        self.running = True

        self.pause_font = pygame.font.Font(None, 32)
        self.audio_font = pygame.font.SysFont(None, 28)
        self.font = pygame.font.SysFont("Times New Roman", 20)

        self.game_over_sound = pygame.mixer.Sound("game_over.mp3")
        self.game_over_sound.set_volume(0.5)  # optional: adjust volume

        self.victory_sound = pygame.mixer.Sound("victory.mp3")
        self.victory_sound.set_volume(0.5)  # optional: adjust volume

        self.navbar = UIOverlay(self.font,self.pause_font,self.audio_font,screen, self.fighter)
        
        self.victory_font = pygame.font.SysFont("arial", 80, bold=True)

        self.box_width, self.box_height = 400, 200
        self.box_x = (SCREEN_WIDTH - self.box_width) // 2
        self.box_y = 100
        self.restart_button = pygame.Rect(self.box_x + 50, self.box_y + 100, 120, 40)
        self.quit_button = pygame.Rect(self.box_x + 230, self.box_y + 100, 120, 40)

    def draw_screen_img(self):
        scene_image = pygame.image.load('fight_scene_wall.jpg')
        scene_image = pygame.transform.scale(scene_image, (SCREEN_WIDTH, SCREEN_HEIGHT - 500))
        scene_bg = pygame.transform.scale(scene_image, (SCREEN_WIDTH, SCREEN_HEIGHT + 40))
        self.screen.blit(scene_bg, (0, 0))

    def pixel_fade_transition(self, screen, main_menu, block_size=20, duration=1000):
        clock = pygame.time.Clock()
        start_time = pygame.time.get_ticks()
        cols = SCREEN_WIDTH // block_size
        rows = SCREEN_HEIGHT // block_size
        pixels = [(x * block_size, y * block_size) for y in range(rows) for x in range(cols)]
        random.shuffle(pixels)

        while True:
            elapsed_time = pygame.time.get_ticks() - start_time
            progress = elapsed_time / duration
            if progress >= 1:
                break

            screen.fill((0, 0, 0))
            main_menu.draw(screen)
            num_pixels = int(len(pixels) * progress)
            for i in range(num_pixels):
                x, y = pixels[i]
                pygame.draw.rect(screen, (0, 0, 0), (x, y, block_size, block_size))
            pygame.display.flip()
            clock.tick(60)

    def run(self):
        clock = pygame.time.Clock()
        pygame.mixer.music.load("fight.mp3")
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)
        not_played_1 = False
        not_played_2 = False
        while self.running:
            delta_time = clock.tick(60) / 1000
            keys = pygame.key.get_pressed()
            self.draw_screen_img()

            if not self.navbar.paused and not self.game_over:
                self.fighter.update(delta_time, keys)
                self.enemy.move(self.fighter)
                self.enemy.update(self.screen, self.fighter)

            if self.navbar.paused:
                overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 0))
                self.screen.blit(overlay, (0, 0))
                paused_text = self.pause_font.render("Paused", True, (255, 255, 255))
                self.screen.blit(paused_text, (self.screen.get_width() // 2 - paused_text.get_width() // 2,
                                            self.screen.get_height() // 2 - paused_text.get_height() // 2))

            if self.fighter.dead:
                self.game_over = True

            if self.enemy.dead and not self.victory:
                self.victory = True
                self.victory_start_time = pygame.time.get_ticks()
                self.enemies_left = 0
                self.enemies_killed = 7

            if self.victory:
                if not not_played_2:
                    self.victory_sound.play()
                    not_played_2 = True
                time_since_victory = pygame.time.get_ticks() - self.victory_start_time
                if time_since_victory < 2000:
                    victory_text = self.victory_font.render("VICTORY!", True, (255, 215, 0))
                    shadow = self.victory_font.render("VICTORY!", True, (0, 0, 0))
                    victory_x = (SCREEN_WIDTH - victory_text.get_width()) // 2
                    self.screen.blit(shadow, (victory_x + 4, 50 + 4))
                    self.screen.blit(victory_text, (victory_x, 50))
                elif abs(self.fighter.x - 936) < 50 and abs(self.fighter.y - 450) < 50:
                    self.pixel_fade_transition(self.screen, self.fighter)
                    pygame.mixer.music.stop()
                    return "completed", self.fighter.health
                
            self.navbar.draw(self.enemies_killed, self.enemies_left)
            self.fighter.draw(self.screen)
            self.enemy.draw(self.screen)
            

            if self.game_over:
                if not not_played_1:
                    self.game_over_sound.play()
                    not_played_1 = True
                overlay = pygame.Surface((self.box_width, self.box_height), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 180))
                self.screen.blit(overlay, (self.box_x, self.box_y))
                pygame.draw.rect(self.screen, WHITE, (self.box_x, self.box_y, self.box_width, self.box_height), 4)

                title = self.font.render("Game Over", True, WHITE)
                self.screen.blit(title, (self.box_x + (self.box_width - title.get_width()) // 2, self.box_y + 20))

                pygame.draw.rect(self.screen, (100, 100, 100), self.restart_button)
                pygame.draw.rect(self.screen, (100, 100, 100), self.quit_button)

                restart_text = self.font.render("Restart", True, WHITE)
                quit_text = self.font.render("Quit", True, WHITE)

                self.screen.blit(restart_text, (self.restart_button.centerx - restart_text.get_width() // 2,
                                                self.restart_button.centery - restart_text.get_height() // 2))
                self.screen.blit(quit_text, (self.quit_button.centerx - quit_text.get_width() // 2,
                                             self.quit_button.centery - quit_text.get_height() // 2))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self.navbar.handle_event(event)
                    if self.game_over:
                        if self.restart_button.collidepoint(mouse_pos):
                            return "restart", None
                        elif self.quit_button.collidepoint(mouse_pos):
                            pygame.quit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_k and not self.navbar.paused:
                        self.fighter.attacking = True
                        self.fighter.attack_timer = self.fighter.attack_duration
                        self.fighter.current_frame = 0
                        self.fighter.attack_check(self.screen, self.enemy)

            pygame.display.update()
