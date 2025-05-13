import pygame
from settings import SCREEN_WIDTH, WHITE

class UIOverlay:
    def __init__(self, font, pause_font, audio_font, screen, player):
        self.font = font
        self.pause_font = pause_font
        self.audio_font = audio_font
        self.screen = screen
        self.player = player
        self.paused = False
        self.audio_muted = False

        self.pause_button = pygame.Rect(20, 10, 100, 40)
        self.audio_button = pygame.Rect(140, 10, 120, 40)

    def draw(self, enemies_killed, enemies_left):
        self._draw_nav_bar(enemies_killed, enemies_left)
        self._draw_pause_button()
        self._draw_audio_button()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.pause_button.collidepoint(mouse_pos):
                self.paused = not self.paused
            elif self.audio_button.collidepoint(mouse_pos):
                self.audio_muted = not self.audio_muted
                pygame.mixer.music.set_volume(0 if self.audio_muted else 0.2)

    def _draw_nav_bar(self, killed, left):
        elapsed_time_ms = pygame.time.get_ticks()
        total_seconds = elapsed_time_ms // 1000
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        time_string_1 = "Time Elapsed:"
        time_string_2 = f"{hours:02}:{minutes:02}:{seconds:02}"
        enemy_count = f"Enemies Left: {left}"
        enemy_kills = f"Enemies Killed: {killed}"

        pygame.draw.rect(self.screen, (30, 30, 30), (0, 0, SCREEN_WIDTH, 60))
        self.screen.blit(self.font.render(time_string_1, True, WHITE), (320, 10))
        self.screen.blit(self.font.render(time_string_2, True, WHITE), (340, 30))
        self.screen.blit(self.font.render(enemy_kills, True, WHITE), (510, 7))
        self.screen.blit(self.font.render(enemy_count, True, WHITE), (510, 30))

        self._draw_hearts(750, 10)

    def _draw_hearts(self, x, y, max_hearts=5):
        full_heart = pygame.image.load("heart.png").convert_alpha()
        full_heart = pygame.transform.scale(full_heart, (30, 30))
        health = self.player.health

        for i in range(max_hearts):
            heart_x = x + i * 45
            if health >= (i + 1) * 20:
                self.screen.blit(full_heart, (heart_x, y))
            elif health > i * 20:
                partial = full_heart.copy()
                partial.fill((200, 0, 0, 180), special_flags=pygame.BLEND_RGBA_MULT)
                self.screen.blit(partial, (heart_x, y))
            else:
                empty = full_heart.copy()
                empty.fill((50, 50, 50, 100), special_flags=pygame.BLEND_RGBA_MULT)
                self.screen.blit(empty, (heart_x, y))

    def _draw_pause_button(self):
        pygame.draw.rect(self.screen, (80, 80, 80), self.pause_button)
        label = "Pause" if not self.paused else "Resume"
        text = self.pause_font.render(label, True, WHITE)
        self.screen.blit(text, (self.pause_button.centerx - text.get_width() // 2,
                                self.pause_button.centery - text.get_height() // 2))

    def _draw_audio_button(self):
        pygame.draw.rect(self.screen, (80, 80, 80), self.audio_button)
        label = "Audio On" if not self.audio_muted else "Audio Off"
        text = self.audio_font.render(label, True, WHITE)
        self.screen.blit(text, (self.audio_button.centerx - text.get_width() // 2,
                                self.audio_button.centery - text.get_height() // 2))
