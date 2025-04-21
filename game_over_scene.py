import pygame
import sys

pygame.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Game Over")

# Load and scale background to fit screen
bg_raw = pygame.image.load("game-over-scene-background.png")
bg = pygame.transform.scale(bg_raw, (screen_width, screen_height))

# Button sizes (bigger buttons)
button_size = (340, 120)

restart_btn = pygame.transform.scale(pygame.image.load("restart_button.png"), button_size)
restart_hover = pygame.transform.scale(pygame.image.load("restart_hover.png"), button_size)
quit_btn = pygame.transform.scale(pygame.image.load("quit_button.png"), button_size)
quit_hover = pygame.transform.scale(pygame.image.load("quit_hover.png"), button_size)

# Button positions (move them closer to each other horizontally and lower)
restart_rect = restart_btn.get_rect(center=(screen_width // 2 - 170, 500))  # Adjusted left
quit_rect = quit_btn.get_rect(center=(screen_width // 2 + 170, 500))  # Adjusted right

clock = pygame.time.Clock()

def game_over_scene():
    while True:
        screen.blit(bg, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True

        # Restart Button
        if restart_rect.collidepoint(mouse_pos):
            screen.blit(restart_hover, restart_rect)
            if click:
                from start_game import start_game_scene  # Replace with your actual function
                start_game_scene()
                return
        else:
            screen.blit(restart_btn, restart_rect)

        # Quit Button
        if quit_rect.collidepoint(mouse_pos):
            screen.blit(quit_hover, quit_rect)
            if click:
                pygame.quit()
                sys.exit()
        else:
            screen.blit(quit_btn, quit_rect)

        pygame.display.flip()
        clock.tick(60)

game_over_scene()
