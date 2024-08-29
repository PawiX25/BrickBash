import pygame
import sys
import random
import os

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Breakout Clone")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10

BALL_SIZE = 10
BALL_SPEED_INCREMENT = 0.1
SCORE_MILESTONE = 10

BRICK_WIDTH = 75
BRICK_HEIGHT = 20
BRICK_ROWS = 5
BRICK_COLUMNS = 10

# Colors for bricks
BRICK_COLORS = [RED, GREEN, BLUE, YELLOW, ORANGE]

# High score management
HIGH_SCORES_FILE = "high_scores.txt"
MAX_HIGH_SCORES = 5  # Number of high scores to track
last_scores = []  # List to track the last 5 scores

# Game variables
score = 0
lives = 3
font = pygame.font.SysFont(None, 36)
game_over = False
paused = False  # Variable to track if the game is paused
last_speed_increase_time = pygame.time.get_ticks()
current_level = 1  # Start at level 1

# Menu variables
menu_active = True
selected_difficulty = 1
difficulty_options = ["Easy", "Medium", "Hard"]

def display_message(text, color, position):
    message = font.render(text, True, color)
    screen.blit(message, position)

def create_brick(row, col):
    color = BRICK_COLORS[row % len(BRICK_COLORS)]
    brick = Brick(col * (BRICK_WIDTH + 5) + 35, row * (BRICK_HEIGHT + 5) + 50, color)
    all_sprites.add(brick)
    bricks.add(brick)

def generate_level(level):
    bricks.empty()  # Clear existing bricks
    all_sprites.remove(*bricks)
    
    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLUMNS):
            if level == 1:
                # Simple pattern for level 1
                create_brick(row, col)
            elif level == 2:
                # Different pattern for level 2
                if row % 2 == 0:
                    create_brick(row, col)
            elif level == 3:
                # More challenging pattern for level 3
                if (row + col) % 2 == 0:
                    create_brick(row, col)

def restart_game(start_level=1):
    global game_over, score, lives, ball, paddle, current_level
    game_over = False
    score = 0
    lives = 3
    ball = Ball()
    paddle = Paddle()
    all_sprites.add(paddle)
    all_sprites.add(ball)
    current_level = start_level
    generate_level(current_level)

def handle_ball_fall():
    global lives
    lives -= 1
    if lives > 0:
        ball.reset()
        paddle.rect.x = (SCREEN_WIDTH - PADDLE_WIDTH) // 2
        paddle.rect.y = SCREEN_HEIGHT - PADDLE_HEIGHT - 10
    else:
        return True
    return False

def set_difficulty(difficulty):
    global PADDLE_SPEED, BALL_SPEED, BRICK_ROWS, BRICK_COLUMNS
    if difficulty == "easy":
        PADDLE_SPEED = 15
        BALL_SPEED = 4
        BRICK_ROWS = 4
        BRICK_COLUMNS = 8
    elif difficulty == "medium":
        PADDLE_SPEED = 10
        BALL_SPEED = 5
        BRICK_ROWS = 5
        BRICK_COLUMNS = 10
    elif difficulty == "hard":
        PADDLE_SPEED = 7
        BALL_SPEED = 6
        BRICK_ROWS = 6
        BRICK_COLUMNS = 12

def load_high_scores():
    if os.path.exists(HIGH_SCORES_FILE):
        with open(HIGH_SCORES_FILE, "r") as file:
            scores = [int(line.strip()) for line in file.readlines()]
            return scores
    return []

def save_high_scores(scores):
    with open(HIGH_SCORES_FILE, "w") as file:
        for score in scores:
            file.write(f"{score}\n")

def update_high_scores(score):
    global last_scores
    last_scores.append(score)
    last_scores = last_scores[-MAX_HIGH_SCORES:]  # Keep only the last 5 scores

    high_scores = load_high_scores()
    high_scores.append(score)
    high_scores.sort(reverse=True)
    high_scores = high_scores[:MAX_HIGH_SCORES]
    save_high_scores(high_scores)

def display_scores():
    # Display the last 5 scores
    for i, last_score in enumerate(reversed(last_scores)):
        display_message(f"Last Score {i+1}: {last_score}", WHITE, (SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT // 2 + 80 + i * 30))
    
    # Display the high score
    high_scores = load_high_scores()
    if high_scores:
        display_message(f"High Score: {high_scores[0]}", YELLOW, (SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT // 2 + 80 + len(last_scores) * 30))

class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([PADDLE_WIDTH, PADDLE_HEIGHT])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = (SCREEN_WIDTH - PADDLE_WIDTH) // 2
        self.rect.y = SCREEN_HEIGHT - PADDLE_HEIGHT - 10

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= PADDLE_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PADDLE_SPEED
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > SCREEN_WIDTH - PADDLE_WIDTH:
            self.rect.x = SCREEN_WIDTH - PADDLE_WIDTH

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([BALL_SIZE, BALL_SIZE])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT // 2
        self.speed_x = BALL_SPEED * random.choice([-1, 1])
        self.speed_y = -BALL_SPEED

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.x <= 0 or self.rect.x >= SCREEN_WIDTH - BALL_SIZE:
            self.speed_x = -self.speed_x
        if self.rect.y <= 0:
            self.speed_y = -self.speed_y

        if pygame.sprite.collide_rect(self, paddle):
            self.speed_y = -self.speed_y
            delta_x = (self.rect.centerx - paddle.rect.centerx) / (PADDLE_WIDTH / 2)
            self.speed_x += delta_x * 2
            self.speed_x = min(max(self.speed_x, -BALL_SPEED * 1.5), BALL_SPEED * 1.5)

        if self.rect.y > SCREEN_HEIGHT:
            return False
        return True

class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface([BRICK_WIDTH, BRICK_HEIGHT])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Initialize sprite groups
all_sprites = pygame.sprite.Group()
bricks = pygame.sprite.Group()

# Create initial game objects
paddle = Paddle()
ball = Ball()
all_sprites.add(paddle)
all_sprites.add(ball)

# Load initial high scores
load_high_scores()

# Main game loop
running = True
while running:
    if menu_active:
        screen.fill(BLACK)

        # Display menu options
        for i, option in enumerate(difficulty_options):
            color = GREEN if i == selected_difficulty else WHITE
            display_message(option, color, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + i * 40))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_difficulty = (selected_difficulty - 1) % len(difficulty_options)
                elif event.key == pygame.K_DOWN:
                    selected_difficulty = (selected_difficulty + 1) % len(difficulty_options)
                elif event.key == pygame.K_RETURN:
                    menu_active = False
                    set_difficulty(difficulty_options[selected_difficulty].lower())
                    generate_level(current_level)
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game_over:
                    restart_game()
                elif event.key == pygame.K_p:  # Toggle pause with 'P'
                    paused = not paused

        if not game_over and not paused:
            all_sprites.update()

            if not ball.update():
                if handle_ball_fall():
                    game_over = True
                    update_high_scores(score)  # Update high scores when the game is over

            brick_collision_list = pygame.sprite.spritecollide(ball, bricks, True)
            if brick_collision_list:
                ball.speed_y = -ball.speed_y
                score += len(brick_collision_list)

            # Check for win condition or advance level
            if len(bricks) == 0:
                current_level += 1
                if current_level <= 3:  # Replace with the total number of levels
                    generate_level(current_level)
                    ball.reset()
                    paddle.rect.x = (SCREEN_WIDTH - PADDLE_WIDTH) // 2
                    paddle.rect.y = SCREEN_HEIGHT - PADDLE_HEIGHT - 10
                else:
                    game_over = True
                    display_message("You Win!", GREEN, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 20))
                    display_message(f"Final Score: {score}", WHITE, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 20))
                    display_message("Press 'R' to Restart", WHITE, (SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT // 2 + 60))
                    update_high_scores(score)  # Update high scores when the game is over

            # Increase ball speed based on score milestones
            if score // SCORE_MILESTONE > (score - len(brick_collision_list)) // SCORE_MILESTONE:
                ball.speed_x += BALL_SPEED_INCREMENT * (1 if ball.speed_x > 0 else -1)
                ball.speed_y += BALL_SPEED_INCREMENT

            # Increase ball speed incrementally over time
            current_time = pygame.time.get_ticks()
            if current_time - last_speed_increase_time > 30000:  # Increase every 30 seconds
                ball.speed_x += BALL_SPEED_INCREMENT * (1 if ball.speed_x > 0 else -1)
                ball.speed_y += BALL_SPEED_INCREMENT
                last_speed_increase_time = current_time

        screen.fill(BLACK)
        all_sprites.draw(screen)

        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        lives_text = font.render(f"Lives: {lives}", True, WHITE)
        screen.blit(lives_text, (10, 50))

        if paused:
            display_message("Paused", WHITE, (SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 - 20))  # Show pause message

        if game_over and len(bricks) > 0:
            display_message("Game Over", RED, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 20))
            display_message(f"Final Score: {score}", WHITE, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 20))
            display_message("Press 'R' to Restart", WHITE, (SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT // 2 + 60))
            display_scores()  # Show last scores and high score

        pygame.display.flip()
        pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
