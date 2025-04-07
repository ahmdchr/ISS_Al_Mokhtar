import pygame
import sys
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from player import Player
from map import Map
from ui import MainMenu
from mokhtar_hero import Fighter
from enemy_bot import Enemy

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Al-Mokhtar")

#set framerate
clock = pygame.time.Clock()
FPS = 60

#define fighters variables
MOD_SIZE = 162
MOD_SCALE = 2
MOD_OFFSET = [55, 10]
MOD_DATA = [MOD_SIZE, MOD_SCALE,MOD_OFFSET]
MOKHTAR_SIZE = 16.6
MOKHTAR_SCALE = 5
MOKHTAR_OFFSET = [0,-18]
MOKHTAR_DATA = [MOKHTAR_SIZE,MOKHTAR_SCALE,MOKHTAR_OFFSET]

#load background image
scene_image = pygame.image.load('./Mainmenu/Background.jpg')

mokhtar_images_sheet = pygame.image.load('Mokhtar_Character_1.png')
mod_images_sheet = pygame.image.load('warrior.png')

MOKHTAR_ANIMATION_STEPS = [3,3,3,4,4,4,1,1,1,1,1,1]
MOD_ANIMATION_STEPS = [10,8,1,7,7,3,7]
MOD_SPEED = 4

def main():
    """Initialize the game and handle the main menu and gameplay loops."""

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
                    gameplay_loop_1(screen)
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

def draw_screen_img():
 scene_bg = pygame.transform.scale(scene_image,(SCREEN_WIDTH,SCREEN_HEIGHT))
 screen.blit(scene_bg,(0,0))

def draw_health_bar(health, x, y):
 ratio = health / 100
 pygame.draw.rect(screen, (255,0,0), (x,y, 400, 30))
 pygame.draw.rect(screen, (255,255,0), (x,y, 400 * ratio, 30))

fighter = Fighter(100,400, False, MOKHTAR_DATA, mokhtar_images_sheet, MOKHTAR_ANIMATION_STEPS)
enemy = Enemy(700,400, True, MOD_DATA, mod_images_sheet, MOD_ANIMATION_STEPS)

font = pygame.font.SysFont("Arial", 36)
text_color = (255, 255, 255)
bg_color = (0, 0, 0)

# Create the text surface
text = font.render("Game Over", True, text_color)

# Set up the rectangle dimensions
rect_width, rect_height = 300, 100
rect_x = (400 - rect_width) // 2
rect_y = (300 - rect_height) // 2

def gameplay_loop_1(screen):
    running = True

    while running:
        clock.tick(FPS)

        draw_screen_img()
        draw_health_bar(fighter.health, 20, 20)
        draw_health_bar(enemy.health, 580, 20)

        fighter.move(SCREEN_WIDTH,SCREEN_HEIGHT,screen,enemy)
        enemy.move(fighter)

        enemy.get_target_status(fighter)

        fighter.update(screen,enemy)
        enemy.update(screen,fighter)
        
        fighter.draw(screen)
        enemy.draw(screen)

        #if fighter.dead:
        #   pygame.draw.rect(screen, (0, 0, 0), (rect_x, rect_y, rect_width, rect_height))
        #    pygame.draw.rect(screen, (255, 255, 255), (rect_x, rect_y, rect_width, rect_height), 5)  
    
        #   text_rect = text.get_rect(center=(rect_x + rect_width // 2, rect_y + rect_height // 2))
        #    screen.blit(text, text_rect)
                
        #if enemy.dead:
        #   pygame.draw.rect(screen, (0, 0, 0), (rect_x, rect_y, rect_width, rect_height))
        #    pygame.draw.rect(screen, (255, 255, 255), (rect_x, rect_y, rect_width, rect_height), 5)  
        
        #    text_rect = text.get_rect(center=(rect_x + rect_width // 2, rect_y + rect_height // 2))
        #    screen.blit(text, text_rect)
  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               running = False
        
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()
