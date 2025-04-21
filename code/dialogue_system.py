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
        processed_dialogue = []
        for item in dialogue_list:
            if isinstance(item, tuple) and len(item) == 2:
                processed_dialogue.append(item)
            elif isinstance(item, str):
                processed_dialogue.append(("", item))
        self.dialogue_list = processed_dialogue
        self.current_dialogue = 0
        self.text_pos = 0
        self.active = True

    def update(self):
        if not self.active or self.current_dialogue >= len(self.dialogue_list):
            return False

        self.text_pos += self.display_speed
        if self.text_pos >= len(self.dialogue_list[self.current_dialogue][1]):
            self.text_pos = len(self.dialogue_list[self.current_dialogue][1])
        return True

    def next_dialogue(self):
        if self.text_pos < len(self.dialogue_list[self.current_dialogue][1]):
            self.text_pos = len(self.dialogue_list[self.current_dialogue][1])
            return False
        else:
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
        current_text = full_text[:self.text_pos]

        y_offset = 20
        if speaker:
            speaker_surface = self.speaker_font.render(f"{speaker}:", True, self.speaker_color)
            surface.blit(speaker_surface, (self.dialogue_box.x + 20, self.dialogue_box.y + y_offset))
            y_offset += 30

        words = current_text.split(' ')
        space_width = self.font.size(' ')[0]
        x, y = self.dialogue_box.x + 20, self.dialogue_box.y + y_offset
        line_height = self.font.get_linesize()

        for word in words:
            word_surface = self.font.render(word, True, self.text_color)
            word_width = word_surface.get_width()
            
            if x + word_width >= self.dialogue_box.right - 20:
                x = self.dialogue_box.x + 20
                y += line_height
            
            surface.blit(word_surface, (x, y + 8))
            x += word_width + space_width

# class DialogueSystem:
#     def __init__(self):
#         self.font = pygame.font.Font(None, 32)
#         self.speaker_font = pygame.font.Font(None, 34)  # Can be different
#         self.dialogue_box = pygame.Rect(50, 650, 900, 100)
#         self.dialogue_list = []  # Now stores tuples of (speaker, text)
#         self.current_dialogue = 0
#         self.text_pos = 0
#         self.display_speed = 2
#         self.active = False
#         self.speaker_color = BROWN  # Brown color for speaker name
#         self.text_color = WHITE     # Color for dialogue text

#     def set_dialogue(self, dialogue_list):
#         """Accepts list of tuples: [(speaker, text), ...] or list of strings"""
#         processed_dialogue = []
#         for item in dialogue_list:
#             if isinstance(item, tuple) and len(item) == 2:
#                 processed_dialogue.append(item)
#             elif isinstance(item, str):
#                 # If no speaker specified, use empty string
#                 processed_dialogue.append(("", item))
#         self.dialogue_list = processed_dialogue
#         self.current_dialogue = 0
#         self.text_pos = 0
#         self.active = True

#     def update(self):
#         if not self.active or self.current_dialogue >= len(self.dialogue_list):
#             return False

#         # Gradually reveal text
#         self.text_pos += self.display_speed
#         if self.text_pos >= len(self.dialogue_list[self.current_dialogue][1]):
#             self.text_pos = len(self.dialogue_list[self.current_dialogue][1])

#         return True

#     def next_dialogue(self):
#         if self.text_pos < len(self.dialogue_list[self.current_dialogue][1]):
#             # Complete current line
#             self.text_pos = len(self.dialogue_list[self.current_dialogue][1])
#             return False  # Not fully advanced yet
            
#         self.current_dialogue += 1
#         self.text_pos = 0
        
#         if self.current_dialogue >= len(self.dialogue_list):
#             self.active = False
#             return True  # Fully completed
            
#         return False  # More dialogues to show

#     def draw(self, surface):
#         if not self.active or self.current_dialogue >= len(self.dialogue_list):
#             return

#         # Draw dialogue box
#         pygame.draw.rect(surface, BEIGE, self.dialogue_box)
#         pygame.draw.rect(surface, WHITE, self.dialogue_box, 3)

#         # Get current speaker and text
#         speaker, full_text = self.dialogue_list[self.current_dialogue]
#         current_text = full_text[:self.text_pos]

#         # Draw speaker name if it exists
#         y_offset = 20
#         if speaker:
#             speaker_surface = self.speaker_font.render(
#                 f"{speaker}:", True, self.speaker_color
#             )
#             surface.blit(speaker_surface, 
#                         (self.dialogue_box.x + 20, 
#                          self.dialogue_box.y + y_offset))
#             y_offset += 30  # Add extra space after speaker

#         # Draw text with word wrapping
#         words = current_text.split(' ')
#         space_width = self.font.size(' ')[0]
#         x, y = self.dialogue_box.x + 20, self.dialogue_box.y + y_offset
#         line_height = self.font.get_linesize()

#         for word in words:
#             word_surface = self.font.render(word, True, self.text_color)
#             word_width = word_surface.get_width()
            
#             if x + word_width >= self.dialogue_box.right - 20:
#                 x = self.dialogue_box.x + 20
#                 y += line_height
            
#             surface.blit(word_surface, (x, y + 8))
#             x += word_width + space_width


# import pygame

# # Dialogue system
# class DialogueSystem:
#     def __init__(self):
#         self.font = pygame.font.Font(None, 32)
#         self.dialogue_box = pygame.Rect(50, 450, 700, 120)
#         self.dialogue_list = []
#         self.current_dialogue = 0
#         self.text_pos = 0
#         self.display_speed = 2
#         self.active = False

#     def set_dialogue(self, dialogue_list):
#         self.dialogue_list = dialogue_list
#         self.current_dialogue = 0
#         self.text_pos = 0
#         self.active = True

#     def update(self):
#         if not self.active or self.current_dialogue >= len(self.dialogue_list):
#             return False

#         # Gradually reveal text
#         self.text_pos += self.display_speed
#         if self.text_pos >= len(self.dialogue_list[self.current_dialogue]):
#             self.text_pos = len(self.dialogue_list[self.current_dialogue])

#         return True

#     def next_dialogue(self):
#         if self.text_pos < len(self.dialogue_list[self.current_dialogue]):
#             # If text is still revealing, show all of it
#             self.text_pos = len(self.dialogue_list[self.current_dialogue])
#         else:
#             # Move to next dialogue
#             self.current_dialogue += 1
#             self.text_pos = 0

#     def draw(self, surface):
#         if not self.active or self.current_dialogue >= len(self.dialogue_list):
#             return

#         # Draw dialogue box
#         pygame.draw.rect(surface, (0, 0, 0), self.dialogue_box)
#         pygame.draw.rect(surface, (255, 255, 255), self.dialogue_box, 3)

#         # Draw text
#         current_text = self.dialogue_list[self.current_dialogue][:self.text_pos]
#         text_surface = self.font.render(current_text, True, (255, 255, 255))
#         surface.blit(text_surface, (self.dialogue_box.x + 20, self.dialogue_box.y + 20))

#         # Draw indicator when dialogue is complete
#         if self.text_pos >= len(self.dialogue_list[self.current_dialogue]):
#             indicator = self.font.render("▼", True, (255, 255, 255))
#             surface.blit(indicator, (self.dialogue_box.x + self.dialogue_box.width - 40, 
#                                     self.dialogue_box.y + self.dialogue_box.height - 40))