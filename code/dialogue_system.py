### Refactored dialogue_system.py
# Simplified dialogue management, improved word wrapping and rendering

import pygame
from settings import BROWN, BEIGE, WHITE

class DialogueSystem:
    def __init__(self):
        self.font = pygame.font.Font(None, 32)
        self.speaker_font = pygame.font.Font(None, 34)
        self.dialogue_box = pygame.Rect(50, 650, 900, 100)

        self.dialogue_list = []
        self.current_dialogue = 0
        self.text_pos = 0
        self.display_speed = 2
        self.active = False

        self.speaker_color = BROWN
        self.text_color = WHITE

    def set_dialogue(self, dialogue_list):
        self.dialogue_list = [(speaker, text) if isinstance(text, str) else ("", text)
                              for speaker, text in (d if isinstance(d, tuple) else ("", d) for d in dialogue_list)]
        self.current_dialogue = 0
        self.text_pos = 0
        self.active = True

    def update(self):
        if not self.active or self.current_dialogue >= len(self.dialogue_list):
            return False

        self.text_pos += self.display_speed
        full_text = self.dialogue_list[self.current_dialogue][1]
        if self.text_pos > len(full_text):
            self.text_pos = len(full_text)
        return True

    def next_dialogue(self):
        if self.text_pos < len(self.dialogue_list[self.current_dialogue][1]):
            self.text_pos = len(self.dialogue_list[self.current_dialogue][1])
            return False

        self.current_dialogue += 1
        self.text_pos = 0
        if self.current_dialogue >= len(self.dialogue_list):
            self.active = False
            return True
        return False

    def draw(self, surface):
        if not self.active or self.current_dialogue >= len(self.dialogue_list):
            return

        pygame.draw.rect(surface, BEIGE, self.dialogue_box)
        pygame.draw.rect(surface, WHITE, self.dialogue_box, 3)

        speaker, full_text = self.dialogue_list[self.current_dialogue]
        text = full_text[:self.text_pos]

        y_offset = 20
        if speaker:
            speaker_surface = self.speaker_font.render(f"{speaker}:", True, self.speaker_color)
            surface.blit(speaker_surface, (self.dialogue_box.x + 20, self.dialogue_box.y + y_offset))
            y_offset += 30

        words = text.split(' ')
        space_width = self.font.size(' ')[0]
        x = self.dialogue_box.x + 20
        y = self.dialogue_box.y + y_offset
        line_height = self.font.get_linesize()

        for word in words:
            word_surface = self.font.render(word, True, self.text_color)
            word_width = word_surface.get_width()

            if x + word_width >= self.dialogue_box.right - 20:
                x = self.dialogue_box.x + 20
                y += line_height

            surface.blit(word_surface, (x, y + 8))
            x += word_width + space_width
