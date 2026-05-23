import pygame
import random
import json
import os

# --- Configuration & Constants ---
SCREEN_WIDTH = 160
SCREEN_HEIGHT = 120
FPS = 60
SAVE_FILE = "level.json" # The file where progress is saved

COLORS = [
    (255, 0, 0), (0, 255, 0), (0, 0, 255), 
    (255, 255, 0), (255, 0, 255), (0, 255, 255)
]

# --- Save/Load Functions ---
def load_level():
    """Reads the level from level.json. Returns 1 if no file exists."""
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as file:
                data = json.load(file)
                loaded_level = data.get("level", 1)
                print(f"Loaded save file! Starting at Level {loaded_level}")
                return loaded_level
        except Exception as e:
            print(f"Error reading save file, starting at Level 1. Error: {e}")
    return 1 # Default level

def save_level(current_level):
    """Saves the current level to level.json."""
    try:
        with open(SAVE_FILE, "w") as file:
            json.dump({"level": current_level}, file)
            print(f"Progress saved: Level {current_level}")
    except Exception as e:
        print(f"Failed to save progress. Error: {e}")

# --- Classes ---
class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("food.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(20, SCREEN_WIDTH - 20)
        self.rect.y = random.randint(20, SCREEN_HEIGHT - 20)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("cat.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed = 2

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:  self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]: self.rect.x += self.speed
        if keys[pygame.K_UP]:    self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:  self.rect.y += self.speed

# --- Initialization ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH * 4, SCREEN_HEIGHT * 4))
pygame.display.set_caption("Eat the Chicken")
display_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# --- Game State ---
level = load_level() # <--- LOAD THE LEVEL HERE
score = 0
count = 0
timer_start = pygame.time.get_ticks()
countdown_seconds = 20
bg_color = random.choice(COLORS)

player = Player()
food_group = pygame.sprite.Group()

def start_level():
    global count, bg_color, timer_start
    count = 0
    bg_color = random.choice(COLORS)
    food_group.empty()
    
    for _ in range(10 + level + 1):
        f = Food()
        food_group.add(f)
    
    timer_start = pygame.time.get_ticks()
    print(f"Level {level} Started!")

start_level()

# --- Main Game Loop ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.update()

    hit_list = pygame.sprite.spritecollide(player, food_group, True)
    for hit in hit_list:
        score += 1
        count += 1
        
        # Level up condition
        if count > 10 + level:
            level += 1
            save_level(level) # <--- SAVE THE LEVEL HERE
            start_level()

    elapsed_time = (pygame.time.get_ticks() - timer_start) // 1000
    remaining_time = max(0, countdown_seconds - elapsed_time)
    
    if remaining_time <= 0:
        print(f"Game Over! Time Ran Out. Final Score: {score}")
        running = False

    # Rendering
    display_surface.fill(bg_color)
    food_group.draw(display_surface)
    display_surface.blit(player.image, player.rect)
    
    scaled_win = pygame.transform.scale(display_surface, (SCREEN_WIDTH * 4, SCREEN_HEIGHT * 4))
    screen.blit(scaled_win, (0, 0))
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()