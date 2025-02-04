import pygame 
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 400
WHITE = (255, 255, 255)
GROUND_Y = HEIGHT - 60
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Load assets
unicorn_img = pygame.image.load("unicorn1.png")  # Add a unicorn sprite
cloud_img = pygame.image.load("rock.png")  # Add cloud obstacles
bg_img = pygame.image.load("background3.jpg")  # Colorful background
powerup_img = pygame.image.load("power_up.png")  # Reward icon

# Resize images
unicorn_img = pygame.transform.scale(unicorn_img, (90, 90))
cloud_img = pygame.transform.scale(cloud_img, (80, 80))
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
powerup_img = pygame.transform.scale(powerup_img, (40, 40))

# Load sound effects
jump_sound = pygame.mixer.Sound("jump.mp3")
game_over_sound = pygame.mixer.Sound("game_over.mp3")

# Load background music
pygame.mixer.music.load("background_music.mp3")

# Game screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
font_large = pygame.font.Font(None, 72)

# Character class
class Unicorn:
    def __init__(self):
        self.images = [pygame.image.load("unicorn1.png"), pygame.image.load("unicorn2.png")]
        self.images = [pygame.transform.scale(img, (90, 90)) for img in self.images]
        self.current_frame = 0
        self.frame_count = 0  # Controls animation speed
        self.x = 100
        self.y = GROUND_Y - 120
        self.vel_y = 0
        self.gravity = 1
        self.is_jumping = False
        self.can_double_jump = True  # Always enabled

    def jump(self):
        if not self.is_jumping:
            self.vel_y = -15
            self.is_jumping = True
            self.can_double_jump = True  # Reset double jump on landing
            jump_sound.play()
        elif self.can_double_jump:
            self.vel_y = -15
            self.can_double_jump = False
            jump_sound.play()

    def update(self):
        self.y += self.vel_y
        self.vel_y += self.gravity
        if self.y >= GROUND_Y - 120:
            self.y = GROUND_Y - 120
            self.is_jumping = False

        # Update animation frame
        self.frame_count += 1
        if self.frame_count % 5 == 0:  # Change image every 10 frames
            self.current_frame = (self.current_frame + 1) % 2

    def draw(self):
        screen.blit(self.images[self.current_frame], (self.x, self.y))

    def collide_with(self, obj):
        unicorn_rect = pygame.Rect(self.x, self.y, 60, 60)
        obj_rect = pygame.Rect(obj.x, obj.y, 50, 50)
        return unicorn_rect.colliderect(obj_rect)

# Obstacle class
class Cloud:
    def __init__(self):
        self.image = cloud_img
        self.x = WIDTH
        self.y = GROUND_Y - 110
        self.speed = 7

    def update(self):
        self.x -= self.speed

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

# Reward class
class PowerUp:
    def __init__(self):
        self.image = powerup_img
        self.x = random.randint(WIDTH // 2, WIDTH)
        self.y = random.randint(50, GROUND_Y - 80)
        self.collected = False

    def update(self):
        if not self.collected:
            self.x -= 5
        if self.x < -40:
            self.collected = True

    def draw(self):
        if not self.collected:
            screen.blit(self.image, (self.x, self.y))

# Game loop
player = Unicorn()
obstacles = []
power_ups = []
score = 0
high_score = 0
coins = 0  # Collectible rewards
game_over = False
game_over_sound_played = False
running = True

pygame.mixer.music.play(-1)

while running:
    screen.blit(bg_img, (0, 0))

    if game_over:
        if not game_over_sound_played:
            game_over_sound.play()
            game_over_sound_played = True

        game_over_text = font_large.render("Game Over", True, RED)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
        restart_text = font.render("Press R to Restart", True, WHITE)
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                player = Unicorn()
                obstacles.clear()
                power_ups.clear()
                score = 0
                coins = 0
                game_over = False
                game_over_sound_played = False
                pygame.mixer.music.play(-1)
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                player.jump()

        if random.randint(1, 80) < 2:
            obstacles.append(Cloud())

        if random.randint(1, 300) < 2:
            power_ups.append(PowerUp())

        player.update()
        player.draw()

        for obstacle in obstacles[:]:
            obstacle.update()
            obstacle.draw()
            if obstacle.x < -50:
                obstacles.remove(obstacle)
                score += 1
            if player.collide_with(obstacle):
                game_over = True

        for power_up in power_ups[:]:
            power_up.update()
            power_up.draw()
            if player.collide_with(power_up):
                power_ups.remove(power_up)
                coins += 1  # Collecting power-ups adds to coins

        score += 0.1
        high_score = max(high_score, int(score))

        score_text = font.render(f"Score: {int(score)}", True, WHITE)
        screen.blit(score_text, (10, 10))
        high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
        screen.blit(high_score_text, (WIDTH - high_score_text.get_width() - 10, 10))
        coins_text = font.render(f"Coins: {coins}", True, WHITE)
        screen.blit(coins_text, (WIDTH // 2, 10))

        pygame.display.update()
    
    clock.tick(30)

pygame.quit()
