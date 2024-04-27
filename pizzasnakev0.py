import pygame
import random

# Initialize Pygame
pygame.init()

# Set screen dimensions (NES resolution)
width, height = 256, 240
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pizza Drop")

# Colors (NES palette approximation)
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
light_gray = (102, 102, 102)
dark_gray = (51, 51, 51)

# Game settings
pizza_size = 16
platform_width = 48
platform_height = 8
platform_x = (width - platform_width) // 2
platform_y = height - 40
speed = 2
score = 0
font = pygame.font.Font(None, 16)  # Simple font for score

# Create game objects
pizza_x = random.randint(0, width - pizza_size)
pizza_y = -pizza_size

# Clock for FPS control
clock = pygame.time.Clock()
fps = 30

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move platform
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and platform_x > 0:
        platform_x -= speed
    if keys[pygame.K_RIGHT] and platform_x < width - platform_width:
        platform_x += speed

    # Move pizza
    pizza_y += speed

    # Check for collision
    if pizza_y + pizza_size > platform_y and pizza_x > platform_x and pizza_x < platform_x + platform_width:
        score += 1
        pizza_x = random.randint(0, width - pizza_size)
        pizza_y = -pizza_size

    # Check if pizza missed platform
    if pizza_y > height:
        print("Game Over! Score:", score)
        running = False

    # Draw everything
    screen.fill(black)  # Black background

    # Platform with simple shading
    pygame.draw.rect(screen, dark_gray, (platform_x, platform_y + 2, platform_width, platform_height))
    pygame.draw.rect(screen, light_gray, (platform_x, platform_y, platform_width, platform_height))

    # Simple pizza representation
    pygame.draw.circle(screen, red, (pizza_x + pizza_size // 2, pizza_y + pizza_size // 2), pizza_size // 2)

    # Score display
    score_text = font.render(f"Score: {score}", True, white)
    screen.blit(score_text, (10, 10))  # Top-left corner

    pygame.display.flip()
    clock.tick(fps)  # Limit frame rate

# Quit Pygame
pygame.quit()
