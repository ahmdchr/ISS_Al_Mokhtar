import pygame
import sys
from settings import SCREEN_WIDTH, SCREEN_HEIGHT,HEART_IMAGE_PATH
from player import Player
from map import Map
from ui import MainMenu
import random
from ui import MainMenu, HealthBar  # Import HealthBar

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Al-Mokhtar")
    clock = pygame.time.Clock()

    # Create game objects
    game_map = Map()
    player = Player(game_map)
    main_menu = MainMenu(game_map)
    health_bar = HealthBar(max_health=5, heart_image_path=HEART_IMAGE_PATH)  # Example: 5 hearts

    while True:
        if main_menu_loop(screen, main_menu):
            gameplay_loop(screen, clock, player, game_map, health_bar)
        else:
            break

    pygame.quit()
    sys.exit()

def main_menu_loop(screen, main_menu):
    """Display and handle interactions with the main menu."""
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  # Exit game
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                main_menu.start_button.check_hover(mouse_pos)
                main_menu.quit_button.check_hover(mouse_pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if main_menu.start_button.hovered:
                    pixel_fade_transition(screen, main_menu)
                    return True  # Start game
                elif main_menu.quit_button.hovered:
                    return False  # Quit game

        main_menu.update()  # Move the background animation
        main_menu.draw(screen)
        pygame.display.flip()
        clock.tick(60)  # Maintain 60 FPS

def gameplay_loop(screen, clock, player, game_map, health_bar):
    """Run the main gameplay loop, handling player movement and game updates."""
    running = True
    while running:
        deltaTime = clock.tick(30) / 1000  # Convert milliseconds to seconds
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Exit the game

        keys = pygame.key.get_pressed()
        player.update(deltaTime, keys)  # Update player state

        game_map.draw(screen, player=player)  # Draw the map with the camera centered on the player
        player.draw(screen)  # Draw the player
        health_bar.draw(screen)

        pygame.display.flip()  # Refresh the screen

def pixel_fade_transition(screen, main_menu, block_size=20, duration=1000):
    """Creates a pixelated fade-out effect before transitioning to the game."""
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    
    cols = SCREEN_WIDTH // block_size
    rows = SCREEN_HEIGHT // block_size

    # Create a shuffled list of pixel positions
    pixels = [(x * block_size, y * block_size) for y in range(rows) for x in range(cols)]
    random.shuffle(pixels)

    while True:
        elapsed_time = pygame.time.get_ticks() - start_time
        progress = elapsed_time / duration

        if progress >= 1:
            break  # End transition

        screen.fill((0, 0, 0))  # Clear screen
        main_menu.draw(screen)  # Draw the menu before applying the effect

        # Calculate how many pixels should be black
        num_pixels = int(len(pixels) * progress)

        # Draw black squares over the menu
        for i in range(num_pixels):
            x, y = pixels[i]
            pygame.draw.rect(screen, (0, 0, 0), (x, y, block_size, block_size))

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
