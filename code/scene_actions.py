### Refactored scene_actions.py
# Structured cutscene steps with clean data format and readability improvements

def get_intro_scene(player, sister, dialogues):
    return [
        {'type': 'dialogue', 'text': [dialogues[0]], 'duration': 2000},
        {'type': 'dialogue', 'text': [dialogues[1]], 'duration': 2000},

        {'type': 'move', 'attack_type': 1, 'character': player, 'target': [572, 270], 'speed': 2, 'duration': 500},
        {'type': 'move', 'character': player, 'target': [560, 280], 'speed': 2, 'duration': 500},

        {
            'type': ['move', 'attack'], 'character': player, 'attack_type': 1,
            'target': [352, 290], 'speed': 2, 'duration': 1600,
            'is_attacking_while_moving': True
        },
        {
            'type': ['dialogue', 'attack'], 'character': player,
            'text': [dialogues[2]], 'attack_type': 2,
            'attack_frames': [1, 2, 3], 'duration': 3000
        },

        {'type': 'dialogue', 'text': [dialogues[3]], 'duration': 2000},
        {'type': 'camera', 'camera_target': [2000, 0], 'duration': 0, 'timer': 7000},
        {'type': 'camera', 'camera_target': [2000, 100], 'duration': 0, 'timer': 1500},
        {'type': 'cutscene', 'duration': 0},
        {'type': ['dialogue'] , 'text': [dialogues[4]], 'duration': 3000},
        {'type': 'move', 'character': sister, 'target': [572, 270], 'speed': 2, 'duration': 500},
        {'type': 'move', 'character': sister, 'target': [550, 285], 'speed': 2, 'duration': 500},
        {'type': 'move', 'character': sister, 'target': [550, 290], 'speed': 2, 'duration': 500},
        {'type': 'move', 'character': sister, 'target': [450, 295], 'speed': 2, 'duration': 500},

        {
            'type': 'dialogue', 'character': player, 'text': [dialogues[5]], 'duration': 3000,
            'attack_idle': {'frames': [0], 'direction': 'right'}
        },
        {
            'type': 'dialogue', 'character': player, 'text': [dialogues[6]], 'duration': 3000,
            'attack_idle': {'frames': [0], 'direction': 'down'}
        },
        {
            'type': 'dialogue', 'character': player, 'text': [dialogues[7]], 'duration': 3000,
            'attack_idle': {'frames': [0], 'direction': 'right'}
        },
        {
            'type': 'dialogue', 'character': player, 'text': [dialogues[8]], 'duration': 3000,
            'attack_idle': {'frames': [0], 'direction': 'left'}
        },

        {'type': 'move', 'character': sister, 'target': [572, 295], 'speed': 2, 'duration': 1500},
        {'type': 'move', 'character': sister, 'target': [572, 245], 'speed': 2, 'duration': 1500},

        {'type': 'wait', 'duration': 300},

        {'type': 'move', 'character': player, 'target': [352, 315], 'speed': 2, 'duration': 1500},
        {'type': 'dialogue', 'text': [dialogues[9]], 'duration': 3000}
    ]
