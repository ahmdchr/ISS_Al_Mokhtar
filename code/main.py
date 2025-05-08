import random
import pygame
import sys
import os

from settings import SCREEN_WIDTH, SCREEN_HEIGHT, SCALED_TILE_SIZE, WHITE, BLACK
from player import Player
from map import Map
from KnightEnemy import KnightEnemy
from ui import MainMenu, HealthBar
from cutscene import Cutscene
from dialogues_text import dialogues
from story_scene import StoryScene
from amira import Character
from enemy_bot import Enemy
from player2 import Player2 

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen_with_margin_top = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + 20))
pygame.display.set_caption("Al-Mokhtar")
clock = pygame.time.Clock()
FPS = 60

scene_image = pygame.image.load('fight_scene_wall.jpg')
scene_image = pygame.transform.scale(scene_image, (SCREEN_WIDTH, SCREEN_HEIGHT - 500))  # optional

ASSET_DIR = "assets"
MAP_DIR = os.path.join(ASSET_DIR, "maps")
ANIMATION_DIR = os.path.join(ASSET_DIR, "animations")
FIRE_DIR = os.path.join(ASSET_DIR, "fire")
UI_DIR = os.path.join(ASSET_DIR, "ui")

# Load your music files
pygame.mixer.music.load("main_menu_music.mp3")  # Music for the main menu
pygame.mixer.music.set_volume(0.4)  # Set the default volume

def main():
    game_map_with_no_margin = Map(False)
    game_map_with_margin = Map(True)
    main_menu = MainMenu(game_map_with_no_margin)
    character = Character(game_map_with_no_margin)

    while True:
        if main_menu_loop(screen, main_menu):
            gameplay_loop(screen, clock, game_map_with_no_margin, game_map_with_margin, character)
        else:
            break

    pygame.quit()
    sys.exit()

def main_menu_loop(screen, main_menu):
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                main_menu.start_button.check_hover(mouse_pos)
                main_menu.quit_button.check_hover(mouse_pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if main_menu.start_button.hovered:
                    pixel_fade_transition(screen, main_menu)
                    return True
                elif main_menu.quit_button.hovered:
                    return False

        main_menu.update()
        main_menu.draw(screen)
        pygame.display.flip()

def gameplay_loop(screen, clock, game_map_1, game_map_2, character):
    running = True
    paused = False
    pressed = False
    game_state = "story"
    game_over = False
    transitioned_to_second_stage = False

    pause_button = pygame.Rect(20, 10, 100, 40)
    audio_button = pygame.Rect(140, 10, 120, 40)
    pause_font = pygame.font.Font(None, 32)
    audio_font = pygame.font.SysFont(None, 28)

    box_width, box_height = 400, 200
    box_x = (SCREEN_WIDTH - box_width) // 2
    box_y = 100  # <-- CENTERED AT TOP

    restart_button = pygame.Rect(box_x + 50, box_y + 100, 120, 40)
    quit_button = pygame.Rect(box_x + 230, box_y + 100, 120, 40)

    font = pygame.font.SysFont("Times New Roman", 20)

    player = Player(game_map_2)
    story_scene = StoryScene(screen, player, character, game_map_1)

    knights = []
    width = game_map_2.visible_width * SCALED_TILE_SIZE

    knight_positions = [(width - 1450, 370), (width - 800, 650), (width - 800, 350), (width - 1150, 320), (width - 1460, 790), (width - 1150, 850)]
    for i, pos in enumerate(knight_positions):
        knight = KnightEnemy(*pos, knight_id=i)
        knights.append(knight)

    # Play the gameplay music after main menu
    pygame.mixer.music.load("gameplay_music_1.mp3")  # Music for the first stage
    pygame.mixer.music.play(-1, 0.0)  # Loop the music indefinitely

    while running:
        delta_time = clock.tick(FPS) / 1000
        story_scene.scene_manager.update()

        number_of_enemies_killed = sum(1 for knight in knights if knight.dead)
        number_of_enemies_left = sum(1 for knight in knights if not knight.dead) + 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pause_button.collidepoint(pygame.mouse.get_pos()):
                    paused = not paused
                if audio_button.collidepoint(pygame.mouse.get_pos()):
                    pressed = not pressed
                    pygame.mixer.music.set_volume(0 if pressed else 0.4)  # Toggle music volume

                if restart_button.collidepoint(pygame.mouse.get_pos()):
                    gameplay_loop(screen, clock, game_map_1, game_map_2, character)
                if quit_button.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k:
                    player.attacking = True
                    player.attack_timer = player.attack_duration
                    player.current_frame = 0
                    player.attack_check(screen, knights)

            if not paused and game_state == "story":
                story_scene.handle_event(event)
            
        if not paused:
            if game_state == "story":
                story_scene.update()
                story_scene.draw()
                if story_scene.done:
                    game_state = "gameplay"
            elif game_state == "gameplay":
                keys = pygame.key.get_pressed()
                player.update(delta_time, keys)
                game_map_2.update_camera(player)
                game_map_2.draw(screen, player=player)

                for knight in knights:
                    knight.update(delta_time, player)
                    knight.draw(screen, game_map_2.camera_x, game_map_2.camera_y)

                # Transition condition
                if not transitioned_to_second_stage and number_of_enemies_killed >= 6:
                    player_x, player_y = game_map_2.camera_x, game_map_2.camera_y
                    target_x, target_y = 1772, 1189

                    if abs(player_x - target_x) < 50 and abs(player_y - target_y) < 50:
                        # Trigger your transition here
                        transitioned_to_second_stage = True  # Mark it as done
                        pixel_fade_transition(screen, game_map_2)  # Or any transition effect
                        pygame.mixer.music.load("gameplay_music_2.mp3")  # Change to second stage music
                        pygame.mixer.music.play(-1, 0.0)  # Loop indefinitely

                if transitioned_to_second_stage:
                    number_of_enemies_killed = 7
                    number_of_enemies_left = 0

                player.draw(screen)

                draw_nav_bar(screen, font, player, number_of_enemies_killed, number_of_enemies_left)
                draw_pause_button(screen, paused, pause_button, pause_font)
                draw_audio_button(screen, pressed, audio_button, audio_font)

                if player.health <= 0:
                    game_over = True

                if game_over:
                    overlay = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
                    overlay.fill((0, 0, 0, 180))
                    screen.blit(overlay, (box_x, box_y))
                    pygame.draw.rect(screen, (255, 255, 255), (box_x, box_y, box_width, box_height), 4)

                    title = font.render("Game Over", True, WHITE)
                    screen.blit(title, (box_x + (box_width - title.get_width()) // 2, box_y + 20))

                    pygame.draw.rect(screen, (100, 100, 100), restart_button)
                    pygame.draw.rect(screen, (100, 100, 100), quit_button)

                    restart_text = font.render("Restart", True, WHITE)
                    quit_text = font.render("Quit", True, WHITE)

                    screen.blit(restart_text, (restart_button.centerx - restart_text.get_width() // 2,
                                            restart_button.centery - restart_text.get_height() // 2))
                    screen.blit(quit_text, (quit_button.centerx - quit_text.get_width() // 2,
                                            quit_button.centery - quit_text.get_height() // 2))

                pygame.display.flip()

        if paused:
            overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
            draw_pause_button(screen, paused, pause_button, pause_font)
            overlay.fill((0, 0, 0, 0))
            screen.blit(overlay, (0, 0))
            paused_text = pause_font.render("Paused", True, (255, 255, 255))
            screen.blit(paused_text, (screen.get_width() // 2 - paused_text.get_width() // 2, screen.get_height() // 2 - paused_text.get_height() // 2))

        if pressed:
            draw_audio_button(screen, pressed, audio_button, audio_font)
            

        pygame.display.flip()

def pixel_fade_transition(screen, main_menu, block_size=20, duration=1000):
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

def draw_hearts(screen, x, y, health, max_hearts=5):
    full_heart = pygame.image.load("heart.png").convert_alpha()
    full_heart = pygame.transform.scale(full_heart, (30, 30))

    for i in range(max_hearts):
        heart_x = x + i * 45

        # Full heart
        if health >= (i + 1) * 20:
            screen.blit(full_heart, (heart_x, y))

        # Partial heart (some health in this chunk)
        elif health > i * 20:
            partial_heart = full_heart.copy()
            partial_heart.fill((200, 0, 0, 180), special_flags=pygame.BLEND_RGBA_MULT)
            screen.blit(partial_heart, (heart_x, y))

        # Empty heart
        else:
            empty_heart = full_heart.copy()
            empty_heart.fill((50, 50, 50, 100), special_flags=pygame.BLEND_RGBA_MULT)
            screen.blit(empty_heart, (heart_x, y))

def draw_nav_bar(screen, font, fighter, killed, left):
    elapsed_time_ms = pygame.time.get_ticks()
    total_seconds = elapsed_time_ms // 1000
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    # Format as HH:MM:SS
    time_string_1 = "Time Elapsed:"
    time_string_2 = f"{hours:02}:{minutes:02}:{seconds:02}"
    Enemey_Count_string = f"Enemies Left: {left}"
    Enemey_Killes_string = f"Enemies Killed: {killed}"

    pygame.draw.rect(screen, (30, 30, 30), (0, 0, SCREEN_WIDTH, 60))  # Dark navbar-like bar

    # Render the timer text
    timer_text_1 = font.render(time_string_1, True, (255, 255, 255))  # White text color
    timer_text_2 = font.render(time_string_2, True, (255, 255, 255))  # White text color
    enemies_text = font.render(Enemey_Killes_string, True, (255, 255, 255))  # White text color
    enemies_text1 = font.render(Enemey_Count_string, True, (255, 255, 255))  # White text color
    screen.blit(timer_text_1, (320, 10))  # Position it in the top-right corner
    screen.blit(timer_text_2, (340, 30))  # Position it in the top-right corner
    screen.blit(enemies_text, (510, 30))
    screen.blit(enemies_text1, (510, 10))

def draw_pause_button(screen, paused, button_rect, font):
    pygame.draw.rect(screen, (200, 200, 200), button_rect)
    pause_text = font.render("Pause" if not paused else "Resume", True, (0, 0, 0))
    screen.blit(pause_text, (button_rect.centerx - pause_text.get_width() // 2,
                            button_rect.centery - pause_text.get_height() // 2))

def draw_audio_button(screen, pressed, button_rect, font):
    pygame.draw.rect(screen, (200, 200, 200), button_rect)
    audio_text = font.render("Audio Off" if pressed else "Audio On", True, (0, 0, 0))
    screen.blit(audio_text, (button_rect.centerx - audio_text.get_width() // 2,
                            button_rect.centery - audio_text.get_height() // 2))

if __name__ == "__main__":
    main()
