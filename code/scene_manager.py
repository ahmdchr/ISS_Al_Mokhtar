### Refactored scene_manager.py
# Modular scene execution, clean handling of actions and transitions

import pygame
import math

class SceneManager:
    def __init__(self, dialogue_system):
        self.dialogue_system = dialogue_system
        self.scenes = {}
        self.current_scene = None
        self.current_action_idx = 0
        self.moving_characters = {}
        self.scene_duration = 0
        self.last_action_time = 0
        self.attacking_characters = {}

    def load_scene(self, name, actions):
        self.scenes[name] = {"actions": actions, "duration": 1000}

    def start_scene(self, name):
        if name in self.scenes:
            self.current_scene = name
            self.current_action_idx = 0
            self._execute_action()

    def _execute_action(self):
        if self.current_scene is None:
            return

        action = self.scenes[self.current_scene]['actions'][self.current_action_idx]
        self.scene_duration = action.get("duration", 3000)
        self.last_action_time = pygame.time.get_ticks()
        action_types = action['type'] if isinstance(action['type'], list) else [action['type']]

        if 'dialogue' in action_types:
            self._start_dialogue(action)
        if 'move' in action_types:
            self._start_movement(action)
        if 'attack' in action_types:
            self._start_attack(action)
        if 'wait' in action_types:
            pass  # Use duration only

    def _start_dialogue(self, action):
        dialogue_data = []
        for line in action['text']:
            if ": " in line:
                speaker, text = line.split(": ", 1)
                dialogue_data.append((speaker, text))
            else:
                dialogue_data.append(("", line))
        self.dialogue_system.set_dialogue(dialogue_data)

    def _start_movement(self, action):
        char = action['character']
        start = [char.x, char.y]
        target = action['target']
        speed = action['speed']
        distance = math.hypot(target[0] - start[0], target[1] - start[1])
        frames = distance / speed
        self.moving_characters[char] = {
            'start_pos': start,
            'target_pos': target,
            'progress': 0,
            'total_frames': frames,
            'speed': speed
        }

    def _start_attack(self, action):
        char = action['character']
        self.attacking_characters[char] = {
            'frames': action.get('attack_frames', [0]),
            'direction': action.get('attack_idle', {}).get('direction', 'down'),
            'duration': action.get('duration', 1000)
        }

    def update(self):
        current_time = pygame.time.get_ticks()

        for char, move in list(self.moving_characters.items()):
            move['progress'] += 1
            ratio = move['progress'] / move['total_frames']
            char.x = move['start_pos'][0] + (move['target_pos'][0] - move['start_pos'][0]) * ratio
            char.y = move['start_pos'][1] + (move['target_pos'][1] - move['start_pos'][1]) * ratio
            if move['progress'] >= move['total_frames']:
                del self.moving_characters[char]

        # Finish attack state automatically
        to_remove = []
        for char, atk in self.attacking_characters.items():
            if current_time - self.last_action_time >= atk['duration']:
                to_remove.append(char)
        for char in to_remove:
            del self.attacking_characters[char]

        # Advance to next action
        if not self.moving_characters and not self.dialogue_system.active:
            if current_time - self.last_action_time > self.scene_duration:
                self.advance_action()

    def advance_action(self):
        if self.current_scene is None:
            return
        self.current_action_idx += 1
        if self.current_action_idx >= len(self.scenes[self.current_scene]['actions']):
            self.current_scene = None
        else:
            self._execute_action()

    def skip_to_last_dialogue(self):
        if self.current_scene is None:
            return

        actions = self.scenes[self.current_scene]['actions']
        last_idx = None
        for i in reversed(range(len(actions))):
            t = actions[i]['type']
            if 'dialogue' in (t if isinstance(t, list) else [t]):
                last_idx = i
                break

        if last_idx is not None:
            self.current_action_idx = last_idx
            self._execute_action()
