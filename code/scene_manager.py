import pygame
import math
from cutscene import Cutscene
import sys

class SceneManager:
    def __init__(self, dialogue_system, screen, game_map):
        self.dialogue_system = dialogue_system
        self.scenes = {}
        self.screen = screen
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
            'duration': 1000
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
        self.scene_duration = action.get("duration", 3000)
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

        self.last_action_time = pygame.time.get_ticks()

    def _show_current_dialogue_line(self):
        if self.current_dialogue_index < len(self.current_dialogue_lines):
            self.dialogue_system.set_dialogue([self.current_dialogue_lines[self.current_dialogue_index]])
            self.current_dialogue_index += 1
            self.last_action_time = pygame.time.get_ticks()

    def update(self):
        current_time = pygame.time.get_ticks()
        
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
            self.cutscene.draw(self.screen)
            pygame.display.flip()



# class SceneManager:
#     def __init__(self, dialogue_system):
#         self.dialogue_system = dialogue_system
#         self.scenes = {}  # Stores scene data
#         self.current_scene = None
#         self.current_action_idx = 0
#         self.scene_timer = 0
#         self.scene_duration = 3000  # Default duration in milliseconds (3 seconds)
#         self.last_action_time = 0

#     def load_scene(self, scene_name, scene_data):
#         """Load a scene with its dialogue/actions."""
#         self.scenes[scene_name] = {
#             'actions': scene_data,
#             'duration': 3000  # Default duration for all actions in this scene
#         }

#     def start_scene(self, scene_name):
#         """Start a specific scene."""
#         if scene_name in self.scenes:
#             self.current_scene = scene_name
#             self.current_action_idx = 0
#             self.last_action_time = pygame.time.get_ticks()
#             self._execute_current_action()

#     def _execute_current_action(self):
#         """Execute the current action in the scene."""
#         if self.current_scene is None:
#             return

#         scene_actions = self.scenes[self.current_scene]['actions']
#         if self.current_action_idx < len(scene_actions):
#             action = scene_actions[self.current_action_idx]
            
#             # Set custom duration if specified in the action
#             if 'duration' in action:
#                 self.scene_duration = action['duration']
#             else:
#                 self.scene_duration = self.scenes[self.current_scene]['duration']
            
#             if action['type'] == 'dialogue':
#                 dialogue_data = []
#                 for line in action['text']:
#                     if ": " in line:
#                         speaker, text = line.split(": ", 1)
#                         dialogue_data.append((speaker, text))
#                     else:
#                         dialogue_data.append(("", line))
                
#                 self.dialogue_system.set_dialogue(dialogue_data)
#                 self.last_action_time = pygame.time.get_ticks()
                


#     # def update(self):
#     #     """Update scene timing and auto-advance if duration elapsed."""
#     #     current_time = pygame.time.get_ticks()
#     #     if (current_time - self.last_action_time > self.scene_duration and 
#     #         self.current_scene is not None):
#     #         self.advance_action()

#     def advance_action(self):
#         """Move to next action in current scene or next scene."""
#         scene_actions = self.scenes[self.current_scene]['actions']
#         self.current_action_idx += 1
        
#         if self.current_action_idx >= len(scene_actions):
#             self.advance_scene()
#         else:
#             self._execute_current_action()

#     def advance_scene(self):
#         """Move to the next scene in sequence."""
#         scene_order = ["intro0", "intro1", "intro2", "intro3", 
#                       "intro4", "intro5", "intro6", "intro7", "intro8"]
    
#         if self.current_scene in scene_order:
#             current_index = scene_order.index(self.current_scene)
#             if current_index + 1 < len(scene_order):
#                 next_scene = scene_order[current_index + 1]
#                 self.start_scene(next_scene)
#             else:
#                 # No more scenes
#                 self.current_scene = None


# class SceneManager:
#     def __init__(self, dialogue_system):
#         self.dialogue_system = dialogue_system
#         self.scenes = {}  # Stores scene data
#         self.current_scene = None
#         self.current_action_idx = 0
#         self.scene_timer = 0
#         self.scene_duration = 3000  # Default duration in milliseconds (3 seconds)
#         self.last_action_time = 0

#     def load_scene(self, scene_name, scene_data):
#         """Load a scene with its dialogue/actions."""
#         self.scenes[scene_name] = {
#             'actions': scene_data,
#             'duration': 3000  # Default duration for all actions in this scene
#         }

#     def start_scene(self, scene_name):
#         """Start a specific scene."""
#         if scene_name in self.scenes:
#             self.current_scene = scene_name
#             self.current_action_idx = 0
#             self.last_action_time = pygame.time.get_ticks()
#             self._execute_current_action()

#     def _execute_current_action(self):
#         """Execute the current action in the scene."""
#         if self.current_scene is None:
#             return

#         scene_actions = self.scenes[self.current_scene]['actions']
#         if self.current_action_idx < len(scene_actions):
#             action = scene_actions[self.current_action_idx]
            
#             # Set custom duration if specified in the action
#             if 'duration' in action:
#                 self.scene_duration = action['duration']
#             else:
#                 self.scene_duration = self.scenes[self.current_scene]['duration']
            
#             if action['type'] == 'dialogue':
#                 dialogue_data = []
#                 for line in action['text']:
#                     if ": " in line:
#                         speaker, text = line.split(": ", 1)
#                         dialogue_data.append((speaker, text))
#                     else:
#                         dialogue_data.append(("", line))
                
#                 self.dialogue_system.set_dialogue(dialogue_data)
#                 self.last_action_time = pygame.time.get_ticks()

#     def update(self):
#         """Update scene timing and auto-advance if duration elapsed."""
#         current_time = pygame.time.get_ticks()
#         if (current_time - self.last_action_time > self.scene_duration and 
#             self.current_scene is not None):
#             self.advance_action()

#     def advance_action(self):
#         """Move to next action in current scene or next scene."""
#         scene_actions = self.scenes[self.current_scene]['actions']
#         self.current_action_idx += 1
        
#         if self.current_action_idx >= len(scene_actions):
#             self.advance_scene()
#         else:
#             self._execute_current_action()

#     def advance_scene(self):
#         """Move to the next scene in sequence."""
#         scene_order = ["intro", "intro1", "intro2", "intro3", 
#                       "intro4", "intro5", "intro6", "intro7", "intro8"]
    
#         if self.current_scene in scene_order:
#             current_index = scene_order.index(self.current_scene)
#             if current_index + 1 < len(scene_order):
#                 next_scene = scene_order[current_index + 1]
#                 self.start_scene(next_scene)
#             else:
#                 # No more scenes
#                 self.current_scene = None

                
# # Scene manager
# class SceneManager:
#     def __init__(self, dialogue_system,player):
#         self.scene_actions = []
#         self.current_action = 0
#         self.action_timer = 0
#         self.dialogue_system = dialogue_system  # Store the dialogue system
#         self.player = player

#     def add_action(self, action_type, duration, **kwargs):
#         """
#         Add an action to the scene
#         action_type: 'move', 'dialogue', 'wait'
#         duration: how many frames this action takes
#         kwargs: additional parameters specific to the action type
#         """
#         self.scene_actions.append({
#             'type': action_type,
#             'duration': duration,
#             'params': kwargs,
#             'completed': False
#         })

#     def update(self, screen):
#         if self.current_action >= len(self.scene_actions):
#             return False

#         action = self.scene_actions[self.current_action]

#         if not action['completed']:
#             # Handle different action types
#             if action['type'] == 'move':
#                 # Movement code stays the same
#                 char_pos = action['params']['character_pos']
#                 target = action['params']['target']
#                 speed = action['params']['speed']

#                 # Calculate movement
#                 dx = target[0] - char_pos[0]
#                 dy = target[1] - char_pos[1]
#                 distance = (dx**2 + dy**2)**0.5

#                 if distance <= speed:
#                     char_pos[0] = target[0]
#                     char_pos[1] = target[1]
#                     self.player.x = char_pos[0]
#                     self.player.y = char_pos[1]
#                     print(f"Self.player.x{self.player.x}")
#                     screen.blit(self.player.image_idle["down"][self.player.current_frame % 3], (self.player.x, self.player.y))
#                     action['completed'] = True
#                 else:
#                     char_pos[0] += dx * speed / distance
#                     char_pos[1] += dy * speed / distance

#             elif action['type'] == 'dialogue':
#                 if 'started' not in action:
#                     self.dialogue_system.set_dialogue(action['params']['text'])  # Use self.dialogue_system
#                     action['started'] = True

#                 if self.action_timer >= action['duration']:
#                     action['completed'] = True

#             elif action['type'] == 'wait':
#                 if self.action_timer >= action['duration']:
#                     action['completed'] = True

#             self.action_timer += 1

#         if action['completed']:
#             self.current_action += 1
#             self.action_timer = 0

#         return True

#     def skip_to_end(self):
#         """Skip to the end of the current scene"""
#         for action in self.scene_actions:
#             if action['type'] == 'move':
#                 char_pos = action['params']['character_pos']
#                 target = action['params']['target']
#                 char_pos[0] = target[0]
#                 char_pos[1] = target[1]

#             action['completed'] = True

#         self.current_action = len(self.scene_actions)
#         # Also deactivate the dialogue system
#         self.dialogue_system.active = False