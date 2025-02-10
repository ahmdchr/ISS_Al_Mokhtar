import pygame
import sys
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from player import Player
from map import Map
from ui import MainMenu

def main():
    """Initialize the game and handle the main menu and gameplay loops."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Al-Mokhtar")
    clock = pygame.time.Clock()

    # Create game objects
    game_map = Map()
    player = Player(game_map)
    main_menu = MainMenu(game_map)

    # Run the main menu; start game if selected, otherwise exit
    while True:
        if main_menu_loop(screen, main_menu):
            gameplay_loop(screen, clock, player, game_map)
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
                    return True  # Start game
                elif main_menu.quit_button.hovered:
                    return False  # Quit game

        main_menu.update()  # Move the background animation
        main_menu.draw(screen)
        pygame.display.flip()
        clock.tick(60)  # Maintain 60 FPS

def gameplay_loop(screen, clock, player, game_map):
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

        game_map.draw(screen)  # Draw the map
        player.draw(screen)  # Draw the player

        pygame.display.flip()  # Refresh the screen
    
    sys.exit()

if __name__ == "__main__":
    main()
