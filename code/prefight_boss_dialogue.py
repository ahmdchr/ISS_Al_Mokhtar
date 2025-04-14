import pygame

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mokhtar Game - Dialogue Scene")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BEIGE = (200, 150, 105)
GRAY = (50, 50, 50)
BROWN = (139, 69, 19)

# Font setup
font = pygame.font.Font(None, 28)
speaker_font = pygame.font.Font(None, 24)  # Smaller font for speaker's name

# Dialogue data
dialogues = [
    ("Knight Commander:", "You’ve got spirit, boy. But spirit won’t save you from the might of Auremagne!"),
    ("Mokhtar:", "I’m not fighting for glory. I’m fighting for my family."),
    ("Knight Commander:" ,"Then die with them!"),

]
dialogue_index = 0

# Buttons
next_button = pygame.Rect(670, 510, 80, 40) 
skip_button = pygame.Rect(670, 420, 80, 30)  # Small skip button above the beige box

running = True
while running:
    screen.fill(WHITE)
    
    # Draw dialogue box
    pygame.draw.rect(screen, BEIGE, (50, 450, 700, 100))
    
    # Get speaker and dialogue text
    speaker, dialogue_text = dialogues[dialogue_index]
    
    # Render speaker's name in brown above the dialogue
    speaker_text = speaker_font.render(speaker, True, BROWN)
    screen.blit(speaker_text, (70, 460))  # Position the speaker's name
    
    # Wrap the dialogue text inside the box
    dialogue_lines = []
    words = dialogue_text.split()
    line = ""
    
    # Split the dialogue into multiple lines if necessary to fit inside the box
    for word in words:
        test_line = line + " " + word if line else word
        if font.size(test_line)[0] <= 650:  # 650 is the width of the beige box
            line = test_line
        else:
            dialogue_lines.append(line)
            line = word
    dialogue_lines.append(line)  # Add the last line
    
    # Calculate the space available for text, starting after the speaker's name
    y_offset = 490  # Start drawing text below the speaker's name
    for line in dialogue_lines:
        line_text = font.render(line, True, WHITE)
        screen.blit(line_text, (70, y_offset))
        y_offset += 30  # Space between lines
    
    # Ensure the text doesn't exceed the beige box's height
    if y_offset > 550:  # The height of the beige box is 100 (450 + 100)
        y_offset = 550  # Keep it inside the box

    # Draw next button
    pygame.draw.rect(screen, BROWN, next_button)
    next_text = font.render("Next", True, WHITE)
    text_x = next_button.x + (next_button.width - next_text.get_width()) // 2
    text_y = next_button.y + (next_button.height - next_text.get_height()) // 2
    screen.blit(next_text, (text_x, text_y))

    # Draw skip button
    pygame.draw.rect(screen, GRAY, skip_button)
    skip_text = font.render("Skip", True, WHITE)
    skip_text_x = skip_button.x + (skip_button.width - skip_text.get_width()) // 2
    skip_text_y = skip_button.y + (skip_button.height - skip_text.get_height()) // 2
    screen.blit(skip_text, (skip_text_x, skip_text_y))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if next_button.collidepoint(event.pos):
                if dialogue_index < len(dialogues) - 1:
                    dialogue_index += 1
            if skip_button.collidepoint(event.pos):  # Skip button action
                dialogue_index = len(dialogues) - 1  # Skip to the last dialogue
    
    pygame.display.flip()

pygame.quit()
