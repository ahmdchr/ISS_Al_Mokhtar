import sys
import pygame
from settings import BROWN, WHITE
from dialogue_system import DialogueSystem
from scene_manager import SceneManager
from scene_actions import get_intro_scene
from dialogues_text import dialogues

class StoryScene:
    def __init__(self, screen, player, sister_character, game_map):
        self.screen = screen
        self.player = player
        self.sister = sister_character
        self.game_map = game_map
        self.dialogue_system = DialogueSystem()
        self.scene_manager = SceneManager(self.dialogue_system)
        
        # Visibility control
        self.show_player = False
        self.show_sister = False
        self.current_action_index = 0  # Track current action index
        
        # UI elements
        self.skip_button = pygame.Rect(869, 610, 80, 40)
        self.next_button = pygame.Rect(866, 707, 80, 40)
        self.hide_next_button = False
        self.skip_font = pygame.font.Font(None, 28)
        self.skip_stage = 0
        
        self.done = False
        self.setup_scenes()

        # Create a semi-transparent overlay surface
        self.overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        self.overlay_opacity = 0  # 0 = fully transparent, 255 = fully opaque
        self.darken_dialogues = True  # Control whether to darken during first dialogues

    def setup_scenes(self):
        """Setup scenes with original dialogues and added movements"""
        # Initial positions
        sister_start_pos = [572, 240]
        player_start_pos = [572, 240]
        
        # Reset character positions
        self.sister.x, self.sister.y = sister_start_pos
        self.player.x, self.player.y = player_start_pos

        scene_actions = get_intro_scene(self.player, self.sister, dialogues)
        self.scene_manager.load_scene("main_intro", scene_actions)
        self.scene_manager.start_scene("main_intro")

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            if self.next_button.collidepoint(mouse_pos) and self.dialogue_system.active:
                if self.dialogue_system.next_dialogue():
                    self.scene_manager.advance_action()
                    self.current_action_index = self.scene_manager.current_action_idx

            if self.skip_button.collidepoint(mouse_pos):
                if self.skip_stage == 0:
                    # First skip: go to last dialogue
                    self.scene_manager.skip_to_last_dialogue()
                    self.skip_stage = 1
                    self.hide_next_button = True  # Hide the next button now
                else:
                    # Second skip: end the scene
                    self.done = True

    def update_visibility(self):
        """Update character visibility and screen opacity"""
        if self.scene_manager.current_scene is None:
            return
            
        # First two dialogues - hide characters and darken screen
        if self.current_action_index < 2:
            self.show_player = False
            self.show_sister = False
            if self.darken_dialogues:
                self.overlay_opacity = 210  # Semi-dark (range 0-255)
            else:
                self.overlay_opacity = 0
        # Third dialogue - show only player, normal screen
        elif self.current_action_index > 8 and self.current_action_index < 19:
            self.show_player = True
            self.show_sister = True
            self.overlay_opacity = 0
        elif self.current_action_index >= 19:
            self.show_player = True
            self.show_sister = False
            self.overlay_opacity = 0
        else:
            self.show_player = True
            self.overlay_opacity = 0

    def draw(self):
        if self.done:
            return

        # Draw game map and characters first
        self.game_map.draw(self.screen)
        
        if self.show_player:
            self.draw_character(self.player)
        if self.show_sister:
            self.draw_character(self.sister)

        # Draw semi-transparent overlay if needed
        if self.overlay_opacity > 0:
            self.overlay.fill((0, 0, 0, self.overlay_opacity))
            self.screen.blit(self.overlay, (0, 0))

        # Draw dialogue UI if active
        if self.dialogue_system.active:
            if not self.hide_next_button:
                self.dialogue_system.draw(self.screen)
                pygame.draw.rect(self.screen, BROWN, self.next_button)
                next_text = self.skip_font.render("Next", True, WHITE)
                self.screen.blit(next_text, (self.next_button.centerx - next_text.get_width()//2, 
                                        self.next_button.centery - next_text.get_height()//2))
            else:
                self.dialogue_system.draw(self.screen)
            

            # Draw skip button (on top of everything)
            pygame.draw.rect(self.screen, (100,100,100), self.skip_button)
            skip_text = self.skip_font.render("Skip", True, (255,255,255))
            self.screen.blit(skip_text, (self.skip_button.centerx - skip_text.get_width()//2,
                                    self.skip_button.centery - skip_text.get_height()//2))

    def update(self):
        if self.done:
            return

        # Update current action index
        self.current_action_index = self.scene_manager.current_action_idx
        
        # Update visibility before other updates
        self.update_visibility()
        
        self.scene_manager.update()

        if self.scene_manager.current_scene is None:
            self.done = True

        if self.dialogue_system.active:
            self.dialogue_system.update()

        if self.scene_manager.current_scene:
            total_actions = len(self.scene_manager.scenes[self.scene_manager.current_scene]['actions'])
            if self.current_action_index >= total_actions - 1:
                self.hide_next_button = True

    def draw_character(self, character):
        current_time = pygame.time.get_ticks()
        attack_data = self.scene_manager.attacking_characters.get(character)
        move_data = self.scene_manager.moving_characters.get(character)

        # IDLE ATTACK ANIMATION
        if attack_data and not move_data:
            direction = attack_data.get("direction", character.facing)
            attack_frames_indices = attack_data.get("frames", [0])
            frames = character.image_attack[direction]
            selected_frames = [frames[i] for i in attack_frames_indices]
            frame = int(current_time / 150) % len(selected_frames)
            self.screen.blit(selected_frames[frame], (character.x, character.y))

        elif move_data:
            # REGULAR MOVEMENT (no attack)
            dx = move_data['target_pos'][0] - move_data['start_pos'][0]
            dy = move_data['target_pos'][1] - move_data['start_pos'][1]
            if abs(dx) > abs(dy):
                character.facing = "right" if dx > 0 else "left"
            else:
                character.facing = "down" if dy > 0 else "up"
            direction = character.facing
            frame = int(current_time / 200) % len(character.image_run[direction])
            self.screen.blit(character.image_run[direction][frame], (character.x, character.y))
            
        else:
            # IDLE
            direction = character.facing
            frame = int(current_time / 200) % len(character.image_idle[direction])
            self.screen.blit(character.image_idle[direction][frame], (character.x, character.y))
