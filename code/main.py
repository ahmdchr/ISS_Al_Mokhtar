import random
import pygame
import sys
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, HEART_IMAGE_PATH
from player import Player
from map import Map
from KnightEnemy import KnightEnemy  # Import the new KnightEnemy class
from ui import MainMenu, HealthBar
from cutscene import Cutscene
from dialogues_text import dialogues
from stroy_scene import StoryScene
from amira import Character

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Al-Mokhtar")

#set framerate
clock = pygame.time.Clock()
FPS = 60

#define fighters variables
MOD_SIZE = 162
MOD_SCALE = 2
MOD_OFFSET = [0, 10]
MOD_DATA = [MOD_SIZE, MOD_SCALE, MOD_OFFSET]
MOKHTAR_SIZE = 16.6
MOKHTAR_SCALE = 5
MOKHTAR_OFFSET = [0,-18]
MOKHTAR_DATA = [MOKHTAR_SIZE, MOKHTAR_SCALE, MOKHTAR_OFFSET]

#load background image
scene_image = pygame.image.load('./Mainmenu/Background.jpg')

# Load sprite sheets for knights
knight_sprite_sheet = pygame.image.load('warrior.png')

# Knight animation steps
KNIGHT_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]  # [idle, run, jump, attack1, attack2, hit, death]

def main():
    """Initialize the game and handle the main menu and gameplay loops."""
    # Create game objects
    game_map = Map()
    player = Player(game_map)
    main_menu = MainMenu(game_map)
    character = Character(game_map)
    cutscene = Cutscene(game_map)  # Create cutscene object

    while True:
        if main_menu_loop(screen, main_menu):
            # Start the cutscene after main menu
            cutscene.start()
            
            # Cutscene loop
            while cutscene.is_playing:
                clock = pygame.time.Clock()
                deltaTime = clock.tick(30) / 1000  # Convert milliseconds to seconds
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            # Allow skipping cutscene with spacebar
                            cutscene.is_playing = False
                
                # Update and draw cutscene
                cutscene.update(deltaTime)
                cutscene.draw(screen)
                
                pygame.display.flip()
            
            # Start normal gameplay after cutscene
            gameplay_loop(screen, clock, player, game_map, character)
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

def gameplay_loop(screen, clock, player, game_map, character):
    running = True
    paused = False
    game_state = "story"

    # Setup pause button
    pause_button = pygame.Rect(20, 20, 100, 40)
    pause_font = pygame.font.Font(None, 32)

    # Setup story scene
    player_1 = Player(game_map)
    story_scene = StoryScene(screen, player_1, character, game_map)
    
    # Create knight enemies at different positions in the map
    knights = []
    knight_positions = [
        (300, 300),   # Top left
        (800, 300),   # Top right
        (300, 600),   # Middle left
        (800, 600),   # Middle right
        (300, 900),   # Bottom left
        (800, 900)    # Bottom right
    ]
    
    for i, pos in enumerate(knight_positions):
        x, y = pos
        knight = KnightEnemy(x, y, i)
        knights.append(knight)
    
    # Create health bar for player
    health_bar = HealthBar(20, 20, player_1.health, 100)

    while running:
        delta_time = clock.tick(60) / 1000  # 60 FPS target, convert to seconds
        
        if game_state == "story":
            story_scene.scene_manager.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if pause_button.collidepoint(mouse_pos):
                    paused = not paused  # Toggle pause

            # Only handle events when not paused
            if not paused and game_state == "story":
                story_scene.handle_event(event)

        # Update logic (only when not paused)
        if not paused:
            if game_state == "story":
                story_scene.update()
                story_scene.draw()
                if story_scene.done:
                    game_state = "gameplay"

            elif game_state == "gameplay":
                keys = pygame.key.get_pressed()
                player_1.update(delta_time, keys)
                
                # Draw the map with the camera centered on the player
                game_map.draw(screen, player=player_1)
                
                # Update and draw all knights
                for knight in knights:
                    # Calculate knight position relative to camera
                    knight_screen_x = knight.rect.x - game_map.camera_x
                    knight_screen_y = knight.rect.y - game_map.camera_y
                    
                    # Store original positions
                    original_x, original_y = knight.rect.x, knight.rect.y
                    
                    # Update knight's rect for screen drawing
                    knight.rect.x = knight_screen_x
                    knight.rect.y = knight_screen_y
                    
                    # Update and draw knight
                    knight.update(delta_time, player_1)
                    knight.draw(screen)
                    
                    # Restore original world coordinates
                    knight.rect.x = original_x
                    knight.rect.y = original_y
                
                # Draw the player
                player_1.draw(screen)
                
                # Update and draw player's health bar
                health_bar.update(player_1.health)
                health_bar.draw(screen)
                
                # Check if player is dead
                if player_1.health <= 0:
                    game_over_font = pygame.font.Font(None, 72)
                    game_over_text = game_over_font.render("Game Over", True, (255, 0, 0))
                    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 
                                             SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
                
                pygame.display.flip()

        # Draw pause button
        pygame.draw.rect(screen, (80, 80, 80), pause_button)
        button_text = "Pause" if not paused else "Resume"
        pause_text = pause_font.render(button_text, True, (255, 255, 255))
        screen.blit(pause_text, (
            pause_button.centerx - pause_text.get_width() // 2,
            pause_button.centery - pause_text.get_height() // 2))

        # Draw pause overlay if paused
        if paused:
            overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))  # Semi-transparent black
            screen.blit(overlay, (0, 0))

            paused_text = pause_font.render("Paused", True, (255, 255, 255))
            screen.blit(paused_text, (
                screen.get_width() // 2 - paused_text.get_width() // 2,
                screen.get_height() // 2 - paused_text.get_height() // 2))

        pygame.display.flip()

    pygame.quit()

def draw_screen_img():
    scene_bg = pygame.transform.scale(scene_image,(SCREEN_WIDTH,SCREEN_HEIGHT))
    screen.blit(scene_bg,(0,0))

def draw_health_bar(health, x, y):
    ratio = health / 1000
    pygame.draw.rect(screen, (255,0,0), (x,y, 400, 30))
    pygame.draw.rect(screen, (255,255,0), (x,y, 400 * ratio, 30))

font = pygame.font.SysFont("Arial", 36)
text_color = (255, 255, 255)
bg_color = (0, 0, 0)

# Create the text surface
text = font.render("Game Over", True, text_color)

# Set up the rectangle dimensions
rect_width, rect_height = 300, 100
rect_x = (400 - rect_width) // 2
rect_y = (300 - rect_height) // 2

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