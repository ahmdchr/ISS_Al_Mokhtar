import math
import random
import pygame
import sys
import os

from settings import SCREEN_WIDTH, SCREEN_HEIGHT,SCALED_TILE_SIZE,WHITE,BLACK
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
from BossFightScene import BossFightScene
from UIOverlay import UIOverlay
from HealthPickup import HealthPickup

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen_with_margin_top = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + 20))
pygame.display.set_caption("Al-Mokhtar")
clock = pygame.time.Clock()
FPS = 60

ASSET_DIR = "assets"
MAP_DIR = os.path.join(ASSET_DIR, "maps")
ANIMATION_DIR = os.path.join(ASSET_DIR, "animations")
FIRE_DIR = os.path.join(ASSET_DIR, "fire")
UI_DIR = os.path.join(ASSET_DIR, "ui")

game_over_sound = pygame.mixer.Sound("game_over.mp3")
game_over_sound.set_volume(0.5)  # optional: adjust volume

def main():
    game_map_with_no_margin = Map(False)
    game_map_with_margin = Map(True)
    main_menu = MainMenu(game_map_with_no_margin)
    character = Character(game_map_with_no_margin)

    while True:
        if main_menu_loop(screen, main_menu):
            pygame.mixer.music.stop()
            gameplay_loop(screen, clock, game_map_with_no_margin, game_map_with_margin, character)
        else:
            break

    pygame.quit()
    sys.exit()

def main_menu_loop(screen, main_menu):
    pygame.mixer.music.load("mainmenu.mp3")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)

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

def cutscene_loop(cutscene):
    while cutscene.is_playing:
        delta_time = clock.tick(FPS) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                cutscene.is_playing = False

        cutscene.update(delta_time)
        cutscene.draw(screen)
        pygame.display.flip()


def gameplay_loop(screen, clock, game_map_1, game_map_2, character):
    running = True
    music_started = False
    not_played = False
    game_state = "story"
    game_over = False
    transitioned_to_second_stage = False

    pause_font = pygame.font.Font(None, 32)
    audio_font = pygame.font.SysFont(None, 28)
    font = pygame.font.SysFont("Times New Roman", 20)

    box_width, box_height = 400, 200
    box_x = (SCREEN_WIDTH - box_width) // 2
    box_y = 100

    restart_button = pygame.Rect(box_x + 50, box_y + 100, 120, 40)
    quit_button = pygame.Rect(box_x + 230, box_y + 100, 120, 40)

    player = Player(game_map_2)
    story_scene = StoryScene(screen, player, character, game_map_1)

    ui_overlay = UIOverlay(font, pause_font, audio_font, screen, player)

    health_pickups = [
        HealthPickup(200, 1500, os.path.join("heart.png")),
        HealthPickup(2800, 200, os.path.join("heart.png")),
        # HealthPickup(1600, 900, os.path.join("heart.png")),
        # HealthPickup(1300, 800, os.path.join("heart.png")),
        # HealthPickup(1600, 900, os.path.join("heart.png"))
    ]

    knights = []
    width = game_map_2.visible_width * SCALED_TILE_SIZE
    knight_positions = [(width - 1450, 370), (width - 800, 650), (width - 800, 350),
                        (width - 1150, 320), (width - 1460, 790), (width - 1150, 850)]
    for i, pos in enumerate(knight_positions):
        knights.append(KnightEnemy(*pos, knight_id=i))

    while running:
        delta_time = clock.tick(FPS) / 1000
        story_scene.scene_manager.update()

        number_of_enemies_killed = sum(1 for knight in knights if knight.dead)
        number_of_enemies_left = sum(1 for knight in knights if not knight.dead) + 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                ui_overlay.handle_event(event)
                if restart_button.collidepoint(pygame.mouse.get_pos()):
                    pygame.mixer.music.stop()
                    gameplay_loop(screen, clock, game_map_1, game_map_2, character)
                if quit_button.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k and not ui_overlay.paused:
                    player.attacking = True
                    player.attack_timer = player.attack_duration
                    player.current_frame = 0
                    player.attack_check(screen, knights)
            if not ui_overlay.paused and game_state == "story":
                story_scene.handle_event(event)
                
        pygame.display.update()

        # Game state logic
       
        if game_state == "story":
            story_scene.update()
            story_scene.draw()
            if story_scene.done:
                game_state = "gameplay"
                pygame.mixer.stop()
        elif game_state == "gameplay":
            if not music_started:
                pygame.mixer.music.load("gameplay.mp3")
                pygame.mixer.music.set_volume(0.2)
                pygame.mixer.music.play(-1)
                music_started = True

            if not ui_overlay.paused:
                keys = pygame.key.get_pressed()
                player.update(delta_time, keys)
                game_map_2.update_camera(player)
                game_map_2.draw(screen, player=player)

                for pickup in health_pickups[:]:
                    if player.rect.colliderect(pickup.rect) and player.health != 100:
                        player.health = min(player.max_health, player.health + pickup.heal_amount)
                        health_pickups.remove(pickup)

                for knight in knights:
                    knight.update(delta_time, player)
                    knight.draw(screen, game_map_2.camera_x, game_map_2.camera_y)

                if not transitioned_to_second_stage and number_of_enemies_killed >= 6:
                    player_x, player_y = game_map_2.camera_x, game_map_2.camera_y
                    if abs(player_x - 1772) < 50 and abs(player_y - 1189) < 50:
                        transitioned_to_second_stage = True
                        pixel_fade_transition(screen, game_map_2)
                        
                        if 'boss_scene' not in locals():
                            boss_scene = BossFightScene(screen, player.health)
                        
                        while True:
                            pygame.mixer.music.stop()
                            result, new_health = boss_scene.run()
                            if result == "restart":
                                boss_scene = BossFightScene(screen, player.health)
                                continue
                            elif result == "completed":
                                player.health = new_health
                                pygame.mixer.music.load("gameplay.mp3")
                                pygame.mixer.music.set_volume(0.2)
                                pygame.mixer.music.play(-1)
                                break

                if transitioned_to_second_stage:
                    number_of_enemies_killed = 7
                    number_of_enemies_left = 0


                if player.health <= 0:
                    game_over = True

                if game_over:
                    if not not_played:
                        game_over_sound.play()
                        not_played = True
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

                player.draw(screen)

                for pickup in health_pickups:
                    pickup.draw(screen, game_map_2.camera_x, game_map_2.camera_y)

            if ui_overlay.paused:
                overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 0))
                screen.blit(overlay, (0, 0))
                paused_text = pause_font.render("Paused", True, (255, 255, 255))
                screen.blit(paused_text, (screen.get_width() // 2 - paused_text.get_width() // 2,
                                            screen.get_height() // 2 - paused_text.get_height() // 2))
            
            ui_overlay.draw(number_of_enemies_killed, number_of_enemies_left)


            

if __name__ == "__main__":
    main()