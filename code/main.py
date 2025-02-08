import pygame
import sys
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from player import Player
from map import Map
from ui import MainMenu

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Al-Mokhtar")
    clock = pygame.time.Clock()

    
    game_map = Map()
    player = Player(game_map)
    main_menu = MainMenu()

    while True:
        if main_menu_loop(screen, main_menu):
            gameplay_loop(screen, clock, player, game_map)
        else:
            break

    pygame.quit()
    sys.exit()

def main_menu_loop(screen, main_menu):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                main_menu.start_button.check_hover(mouse_pos)
                main_menu.quit_button.check_hover(mouse_pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if main_menu.start_button.hovered:
                    return True
                elif main_menu.quit_button.hovered:
                    return False

        main_menu.draw(screen)
        pygame.display.flip()

def gameplay_loop(screen, clock, player, game_map):
    running = True
    while running:
        deltaTime = clock.tick(30) / 1000
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        player.update(deltaTime, keys)

        game_map.draw(screen)
        player.draw(screen)

        pygame.display.flip()
    sys.exit()

if __name__ == "__main__":
    main()