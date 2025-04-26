import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BEIGE, BROWN, WHITE

class DialogueScene:
    def __init__(self, screen, dialogues, on_complete=None):
        self.screen = screen
        self.dialogues = dialogues
        self.dialogue_index = 0
        self.font = pygame.font.Font(None, 28)
        self.speaker_font = pygame.font.Font(None, 24)

        self.dialogue_box = pygame.Rect(50, SCREEN_HEIGHT - 150, SCREEN_WIDTH - 100, 100)
        self.next_button = pygame.Rect(SCREEN_WIDTH - 130, SCREEN_HEIGHT - 90, 80, 40)
        self.skip_button = pygame.Rect(SCREEN_WIDTH - 130, SCREEN_HEIGHT - 190, 80, 30)

        self.running = True
        self.on_complete = on_complete

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.next_button.collidepoint(event.pos):
                if self.dialogue_index < len(self.dialogues) - 1:
                    self.dialogue_index += 1
                else:
                    self.running = False
                    if self.on_complete:
                        self.on_complete()
            if self.skip_button.collidepoint(event.pos):
                self.dialogue_index = len(self.dialogues) - 1

    def draw(self):
        self.screen.fill(WHITE)

        # Draw dialogue box
        pygame.draw.rect(self.screen, BEIGE, self.dialogue_box)

        speaker, dialogue_text = self.dialogues[self.dialogue_index]

        # Render speaker
        speaker_text = self.speaker_font.render(speaker, True, BROWN)
        self.screen.blit(speaker_text, (self.dialogue_box.x + 20, self.dialogue_box.y + 10))

        # Word wrapping
        words = dialogue_text.split()
        line = ""
        lines = []
        for word in words:
            test_line = line + " " + word if line else word
            if self.font.size(test_line)[0] < self.dialogue_box.width - 40:
                line = test_line
            else:
                lines.append(line)
                line = word
        lines.append(line)

        y_offset = self.dialogue_box.y + 40
        for l in lines:
            rendered = self.font.render(l, True, WHITE)
            self.screen.blit(rendered, (self.dialogue_box.x + 20, y_offset))
            y_offset += 30

        # Draw buttons
        pygame.draw.rect(self.screen, BROWN, self.next_button)
        next_text = self.font.render("Next", True, WHITE)
        self.screen.blit(next_text, (self.next_button.centerx - next_text.get_width()//2, self.next_button.centery - next_text.get_height()//2))

        pygame.draw.rect(self.screen, (80,80,80), self.skip_button)
        skip_text = self.font.render("Skip", True, WHITE)
        self.screen.blit(skip_text, (self.skip_button.centerx - skip_text.get_width()//2, self.skip_button.centery - skip_text.get_height()//2))

        pygame.display.flip()

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)
            self.draw()
            clock.tick(60)
