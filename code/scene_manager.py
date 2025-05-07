import pygame
import math
from cutscene import Cutscene
import sys
from settings import SCREEN_HEIGHT,SCREEN_WIDTH,SCALED_TILE_SIZE
from camera import Camera
from player import Player

class SceneManager:
    def __init__(self, dialogue_system, screen, game_map):
        self.dialogue_system = dialogue_system
        self.scenes = {}
        self.screen = screen
        self.camera = Camera(game_map,12,screen)
        self.map = game_map
        self.map_width = game_map.visible_width * SCALED_TILE_SIZE
        self.map_height = game_map.visible_height * SCALED_TILE_SIZE
        self.camera_target = None
        self.camera_duration = 0
        self.camera_start_time = 0
        self.camera_start_pos = (0, 0)
        self.cutscene = Cutscene(game_map)
        self.current_scene = None
        self.current_action_idx = 0
        self.scene_timer = 0
        self.moving_characters = {}
        self.scene_duration = 0
        self.last_action_time = 0
        self.current_dialogue_lines = []
        self.current_dialogue_index = 0
        self.attacking_characters = {}

    def load_scene(self, scene_name, scene_data):
        self.scenes[scene_name] = {
            'actions': scene_data,
            'duration': 0
        }

    def start_scene(self, scene_name):
        if scene_name in self.scenes:
            self.current_scene = scene_name
            self.current_action_idx = 0
            self.last_action_time = pygame.time.get_ticks()
            self._execute_current_action()

    def _execute_current_action(self):
        if self.current_scene is None:
            return

        action = self.scenes[self.current_scene]['actions'][self.current_action_idx]
        self.scene_duration = action.get("duration", 0)
        types = action['type'] if isinstance(action['type'], list) else [action['type']]
        self.last_action_time = pygame.time.get_ticks()

        # Dialogue setup
        if 'dialogue' in types:
            dialogue_data = []
            for line in action['text']:
                if ": " in line:
                    speaker, text = line.split(": ", 1)
                    dialogue_data.append((speaker, text))
                else:
                    dialogue_data.append(("", line))
            self.dialogue_system.set_dialogue(dialogue_data)

            # Optional attack_idle during dialogue
            if 'character' in action and 'attack_idle' in action:
                character = action['character']
                self.attacking_characters[character] = {
                    'start_time': self.last_action_time,
                    'duration': self.scene_duration,
                    'frames': action['attack_idle'].get('frames', [0]),
                    'direction': action['attack_idle'].get('direction', character.facing),
                    'is_attacking_while_moving': False
                }
            elif 'character' in action:
                character = action['character']
                self.attacking_characters.pop(character, None)

        # Move setup
        if 'move' in types:
            character = action['character']
            target = action['target']
            speed = action['speed']
            start_pos = [character.x, character.y]
            distance = math.hypot(target[0] - start_pos[0], target[1] - start_pos[1])
            frames_needed = distance / speed

            self.moving_characters[character] = {
                'start_pos': start_pos,
                'target_pos': target,
                'progress': 0,
                'total_frames': frames_needed,
                'speed': speed
            }

        # ✅ Handle attack (while moving or stationary)
        if 'attack' in types:
            character = action['character']
            self.attacking_characters[character] = {
                'start_time': self.last_action_time,
                'duration': self.scene_duration,
                'attack_type': action.get('attack_type', 1),
                'direction': action.get('direction', character.facing),
                'is_attacking_while_moving': action.get('is_attacking_while_moving', False),
                'frames': [0, 3] if action.get('attack_type', 1) == 1 else [1, 2]
            }

        if 'wait' in types:
            # Simply wait for the specified duration
            pass

        if 'cutscene' in types:
            self.cutscene.start()
            self.cutscene_loop()

        if 'camera' in types:
            cam_target = action.get("camera_target", (0, 0))
            timer = action.get("timer", 0)
            self.camera.set_camera_position(cam_target[0], cam_target[1])
            self.camera_loop(timer)

        self.last_action_time = pygame.time.get_ticks()

    def _show_current_dialogue_line(self):
        if self.current_dialogue_index < len(self.current_dialogue_lines):
            self.dialogue_system.set_dialogue([self.current_dialogue_lines[self.current_dialogue_index]])
            self.current_dialogue_index += 1
            self.last_action_time = pygame.time.get_ticks()

    def update(self):
        current_time = pygame.time.get_ticks()
        self.camera.update_camera()

        # Update moving characters
        for character, move_data in list(self.moving_characters.items()):
            move_data['progress'] += 1
            progress_ratio = move_data['progress'] / move_data['total_frames']
            
            character.x = move_data['start_pos'][0] + (move_data['target_pos'][0] - move_data['start_pos'][0]) * progress_ratio
            character.y = move_data['start_pos'][1] + (move_data['target_pos'][1] - move_data['start_pos'][1]) * progress_ratio
            
            if move_data['progress'] >= move_data['total_frames']:
                del self.moving_characters[character]

        # Clear attack after duration
        for character in list(self.attacking_characters):
            attack_data = self.attacking_characters[character]
            if current_time - attack_data['start_time'] > attack_data['duration']:
                del self.attacking_characters[character]
        
        # Handle dialogue progression
        if self.dialogue_system.active:
            if current_time - self.last_action_time > self.scene_duration:
                # If there are more lines in current dialogue action, show next one immediately
                if self.current_dialogue_index < len(self.current_dialogue_lines):
                    self._show_current_dialogue_line()
                else:
                    # No more lines in this dialogue action
                    self.dialogue_system.active = False
                    self.advance_action()
        # Handle non-dialogue actions
        elif not self.moving_characters:
            if current_time - self.last_action_time > self.scene_duration:
                self.advance_action()
        
    def advance_action(self):
        if self.current_scene is None:
            return  # 💡 Early return to prevent KeyError
        
        self.current_action_idx += 1
        
        if self.current_action_idx >= len(self.scenes[self.current_scene]['actions']):
            self.current_scene = None
        else:
            self._execute_current_action()

    def skip_to_last_dialogue(self):
        if self.current_scene is None:
            return

        actions = self.scenes[self.current_scene]['actions']
        
        # Find the last dialogue index
        last_dialogue_idx = None
        for i in reversed(range(len(actions))):
            types = actions[i]['type'] if isinstance(actions[i]['type'], list) else [actions[i]['type']]
            if 'dialogue' in types:
                last_dialogue_idx = i - 1
                break

        if last_dialogue_idx is not None:
            self.current_action_idx = last_dialogue_idx
            self._execute_current_action()

    def cutscene_loop(self):
        clock = pygame.time.Clock()
        while self.cutscene.is_playing:
            delta_time = clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.cutscene.is_playing = False

            self.cutscene.update(delta_time)
            self.cutscene.draw(self.screen,delta_time)
            pygame.display.flip()

    def camera_loop(self,duration):
        start_time = pygame.time.get_ticks()  # Record when the loop starts
        clock = pygame.time.Clock()
        player = Player(self.map)
        player.x = 352
        player.y = 290
        player.direction = "left"
        player.attacking = "True"

        while self.camera.is_playing:
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - start_time
            delta_time = clock.tick(60) / 1000  # Convert to seconds

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.camera.is_playing = False

            if elapsed_time > duration:
                self.camera.is_playing = False
            
            self.camera.update_camera()
            self.camera.draw(self.screen)
           

            player.update(delta_time, pygame.key.get_pressed())
            player.draw(self.screen)

            pygame.display.flip()
