import pygame
import sys
import random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Breakout Clone")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
PADDLE_SPEED = 10

BALL_SIZE = 10
BALL_SPEED = 5

BRICK_WIDTH = 75
BRICK_HEIGHT = 20
BRICK_ROWS = 5
BRICK_COLUMNS = 10

score = 0
font = pygame.font.SysFont(None, 36)
game_over = False

def display_message(text, color, position):
    message = font.render(text, True, color)
    screen.blit(message, position)

def restart_game():
    global game_over, score, ball, paddle, bricks
    game_over = False
    score = 0
    ball = Ball()
    paddle = Paddle()
    all_sprites.add(paddle)
    all_sprites.add(ball)
    bricks.empty()
    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLUMNS):
            brick = Brick(col * (BRICK_WIDTH + 5) + 35, row * (BRICK_HEIGHT + 5) + 50)
            all_sprites.add(brick)
            bricks.add(brick)

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
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT // 2
        self.speed_x = BALL_SPEED * random.choice([-1, 1])
        self.speed_y = -BALL_SPEED

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Ball collision with walls
        if self.rect.x <= 0 or self.rect.x >= SCREEN_WIDTH - BALL_SIZE:
            self.speed_x = -self.speed_x
        if self.rect.y <= 0:
            self.speed_y = -self.speed_y

        # Ball collision with paddle
        if pygame.sprite.collide_rect(self, paddle):
            self.speed_y = -self.speed_y

        # Ball falls off screen
        if self.rect.y > SCREEN_HEIGHT:
            return False
        return True

class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([BRICK_WIDTH, BRICK_HEIGHT])
        self.image.fill(RED)
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
for row in range(BRICK_ROWS):
    for col in range(BRICK_COLUMNS):
        brick = Brick(col * (BRICK_WIDTH + 5) + 35, row * (BRICK_HEIGHT + 5) + 50)
        all_sprites.add(brick)
        bricks.add(brick)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                restart_game()

    if not game_over:
        all_sprites.update()

        if not ball.update():  # Check if ball is out of play
            game_over = True  # End the game if ball falls off screen

        brick_collision_list = pygame.sprite.spritecollide(ball, bricks, True)
        if brick_collision_list:
            ball.speed_y = -ball.speed_y
            score += len(brick_collision_list)

    screen.fill(BLACK)
    all_sprites.draw(screen)

    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    if game_over:
        display_message("Game Over", RED, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 20))
        display_message(f"Final Score: {score}", WHITE, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 20))
        display_message("Press 'R' to Restart", WHITE, (SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT // 2 + 60))

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()