### Cleaned and Fixed Version of main.py and Critical Components
# Refactored to fix player freeze, missing attributes, map bugs, and cleaned structure

import random
import pygame
import sys
import os

from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from player import Player
from map import Map
from KnightEnemy import KnightEnemy
from ui import MainMenu, HealthBar
from cutscene import Cutscene
from dialogues_text import dialogues
from story_scene import StoryScene
from amira import Character

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Al-Mokhtar")
clock = pygame.time.Clock()
FPS = 60

ASSET_DIR = "assets"
MAP_DIR = os.path.join(ASSET_DIR, "maps")
ANIMATION_DIR = os.path.join(ASSET_DIR, "animations")
FIRE_DIR = os.path.join(ASSET_DIR, "fire")
UI_DIR = os.path.join(ASSET_DIR, "ui")

def main():
    game_map = Map()
    player = Player(game_map)
    main_menu = MainMenu(game_map)
    character = Character(game_map)
    cutscene = Cutscene(game_map)

    while True:
        if main_menu_loop(screen, main_menu):
            # cutscene.start()
            # cutscene_loop(cutscene)
            gameplay_loop(screen, clock, game_map, character)
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

def gameplay_loop(screen, clock, game_map, character):
    running = True
    paused = False
    game_state = "story"

    pause_button = pygame.Rect(20, 20, 100, 40)
    pause_font = pygame.font.Font(None, 32)

    player = Player(game_map)
    story_scene = StoryScene(screen, player, character, game_map)


    knights = []
    knight_positions = [(300, 300), (800, 300), (300, 600), (800, 600), (300, 900), (800, 900)]
    for i, pos in enumerate(knight_positions):
        knight = KnightEnemy(*pos, knight_id=i)
        knights.append(knight)

    health_bar = HealthBar(20, 20, player.health, 100)

    while running:
        delta_time = clock.tick(FPS) / 1000
        story_scene.scene_manager.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pause_button.collidepoint(pygame.mouse.get_pos()):
                    paused = not paused
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k:
                    player.attacking = True
                    player.attack_timer = player.attack_duration
                    player.current_frame = 0
                    player.attack_check(knights)
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
                game_map.update_camera(player)
                game_map.draw(screen, player=player)

                for knight in knights:
                    knight.update(delta_time, player)
                    knight.draw(screen, game_map.camera_x, game_map.camera_y)

                player.draw(screen)
                health_bar.update(player.health)
                health_bar.draw(screen)

                if player.health <= 0:
                    game_over_font = pygame.font.Font(None, 72)
                    game_over_text = game_over_font.render("Game Over", True, (255, 0, 0))
                    screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2 - game_over_text.get_height()//2))

                pygame.display.flip()

        pygame.draw.rect(screen, (80, 80, 80), pause_button)
        button_text = "Pause" if not paused else "Resume"
        pause_text = pause_font.render(button_text, True, (255, 255, 255))
        screen.blit(pause_text, (pause_button.centerx - pause_text.get_width()//2, pause_button.centery - pause_text.get_height()//2))

        if paused:
            overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            screen.blit(overlay, (0, 0))
            paused_text = pause_font.render("Paused", True, (255, 255, 255))
            screen.blit(paused_text, (screen.get_width()//2 - paused_text.get_width()//2, screen.get_height()//2 - paused_text.get_height()//2))

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

if __name__ == "__main__":
    main()
