import pygame

pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Al-Mokhtar")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Load images and scale them
def load_images(path, frames, size=(69, 69)):
    return [pygame.transform.scale(pygame.image.load(f"{path}{i+1}.png"), size) for i in range(frames)]

image_idle_down = load_images('idle_animation/hero_down/hero_down_', 3)
image_idle_left = load_images('idle_animation/hero_left/hero_left_', 3)
image_idle_right = load_images('idle_animation/hero_right/hero_right_', 3)
image_idle_up = load_images('idle_animation/hero_up/hero_up_', 3)

image_run_down = load_images('run_animation/hero_down/hero_down_', 4)
image_run_left = load_images('run_animation/hero_left/hero_left_', 4)
image_run_right = load_images('run_animation/hero_right/hero_right_', 4)
image_run_up = load_images('run_animation/hero_up/hero_up_', 4)

# Player properties
player_speed = 300
x, y = 100, 100
direction = 0  # 0: down, 1: left, 2: right, 3: up
current_frame = 0
animation_speed = 0.1
animation_timer = 0

running = True
while running:
    deltaTime = clock.tick(30) / 1000
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Handle movement and direction
    if keys[pygame.K_LEFT] or keys[pygame.K_q]:
        direction = 1
        x -= player_speed * deltaTime
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        direction = 2
        x += player_speed * deltaTime
    elif keys[pygame.K_UP] or keys[pygame.K_z]:
        direction = 3
        y -= player_speed * deltaTime
    elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
        direction = 0
        y += player_speed * deltaTime

    # Update animation frame
    animation_timer += deltaTime
    if animation_timer >= animation_speed:
        animation_timer = 0
        current_frame = (current_frame + 1) % 4  # Assuming 4 frames for running animations

    # Determine which animation to play
    if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]:
        if direction == 0:
            screen.blit(image_run_down[current_frame], (x, y))
        elif direction == 1:
            screen.blit(image_run_left[current_frame], (x, y))
        elif direction == 2:
            screen.blit(image_run_right[current_frame], (x, y))
        elif direction == 3:
            screen.blit(image_run_up[current_frame], (x, y))
    else:
        if direction == 0:
            screen.blit(image_idle_down[current_frame % 3], (x, y))
        elif direction == 1:
            screen.blit(image_idle_left[current_frame % 3], (x, y))
        elif direction == 2:
            screen.blit(image_idle_right[current_frame % 3], (x, y))
        elif direction == 3:
            screen.blit(image_idle_up[current_frame % 3], (x, y))

    pygame.display.flip()

pygame.quit()