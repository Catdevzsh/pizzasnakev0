import pygame
import random
from array import array

# Initialize Pygame and its components
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

# Define function to generate beep sounds
def generate_beep_sound(frequency=440, duration=0.1):
    sample_rate = pygame.mixer.get_init()[0]
    max_amplitude = 2 ** (abs(pygame.mixer.get_init()[1]) - 1) - 1
    samples = int(sample_rate * duration)
    wave = [int(max_amplitude * ((i // (sample_rate // frequency)) % 2)) for i in range(samples)]
    sound = pygame.mixer.Sound(buffer=array('h', wave))
    sound.set_volume(0.1)
    return sound

# Sound effects for game events
catch_sound = generate_beep_sound(523.25, 0.1)  # Sound for catching a pizza
miss_sound = generate_beep_sound(349.23, 0.2)   # Sound for missing a pizza

# Set screen dimensions (NES resolution)
width, height = 256, 240
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pizza Drop")

# Colors and game settings
black, white, red = (0, 0, 0), (255, 255, 255), (255, 0, 0)
dark_gray, light_gray = (51, 51, 51), (102, 102, 102)
pizza_size = 16
platform_width, platform_height = 48, 8
platform_x = (width - platform_width) // 2
platform_y = height - 40
speed, score = 2, 0
font = pygame.font.Font(None, 16)

# Create pizza starting position
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

    # Platform movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and platform_x > 0:
        platform_x -= speed
    if keys[pygame.K_RIGHT] and platform_x < width - platform_width:
        platform_x += speed

    # Pizza movement
    pizza_y += speed

    # Collision detection
    if pizza_y + pizza_size > platform_y and platform_x < pizza_x + pizza_size < platform_x + platform_width:
        score += 1
        catch_sound.play()  # Play sound on catching a pizza
        pizza_x = random.randint(0, width - pizza_size)
        pizza_y = -pizza_size

    # Check if pizza misses platform
    if pizza_y > height:
        miss_sound.play()  # Play sound on missing a pizza
        print("Game Over! Score:", score)
        running = False

    # Drawing the game elements
    screen.fill(black)
    pygame.draw.rect(screen, dark_gray, (platform_x, platform_y + 2, platform_width, platform_height))
    pygame.draw.rect(screen, light_gray, (platform_x, platform_y, platform_width, platform_height))
    pygame.draw.circle(screen, red, (pizza_x + pizza_size // 2, pizza_y + pizza_size // 2), pizza_size // 2)
    score_text = font.render(f"Score: {score}", True, white)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
