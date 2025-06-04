import pygame
import random
import time

# Init
pygame.init()
WIDTH, HEIGHT = 800, 600
BLOCK_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🐍 Classic Snake Game")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont("arial", 25)
big_font = pygame.font.SysFont("impact", 60)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 100, 0)
RED = (255, 50, 50)
YELLOW = (255, 255, 0)
GRAY = (100, 100, 100)

high_score = 0

def draw_snake_block(pos, is_head=False):
    color = DARK_GREEN if is_head else GREEN
    pygame.draw.rect(screen, color, (*pos, BLOCK_SIZE, BLOCK_SIZE), border_radius=4)
    if is_head:
        eye1 = (pos[0] + 4, pos[1] + 5)
        eye2 = (pos[0] + 4, pos[1] + 14)
        pygame.draw.circle(screen, BLACK, eye1, 2)
        pygame.draw.circle(screen, BLACK, eye2, 2)

def draw_apple(pos):
    pygame.draw.circle(screen, RED, (pos[0] + BLOCK_SIZE // 2, pos[1] + BLOCK_SIZE // 2), BLOCK_SIZE // 2)

def draw_traps():
    for stone in traps:
        pygame.draw.rect(screen, GRAY, (*stone, BLOCK_SIZE, BLOCK_SIZE), border_radius=2)

class Snake:
    def __init__(self):
        self.body = [(100, 100), (80, 100), (60, 100)]
        self.direction = "RIGHT"

    def move(self):
        x, y = self.body[0]
        if self.direction == "UP": y -= BLOCK_SIZE
        elif self.direction == "DOWN": y += BLOCK_SIZE
        elif self.direction == "LEFT": x -= BLOCK_SIZE
        elif self.direction == "RIGHT": x += BLOCK_SIZE
        new_head = (x % WIDTH, y % HEIGHT)
        self.body.insert(0, new_head)
        self.body.pop()

    def grow(self):
        self.body.append(self.body[-1])

    def change_direction(self, new_dir):
        opposite = {"UP": "DOWN", "DOWN": "UP", "LEFT": "RIGHT", "RIGHT": "LEFT"}
        if new_dir != opposite[self.direction]:
            self.direction = new_dir

    def draw(self):
        for i, seg in enumerate(self.body):
            draw_snake_block(seg, is_head=(i == 0))

    def check_collision(self):
        return self.body[0] in self.body[1:]

def random_pos(exclude=None):
    while True:
        pos = (random.randrange(0, WIDTH, BLOCK_SIZE), random.randrange(0, HEIGHT, BLOCK_SIZE))
        if not exclude or pos not in exclude:
            return pos

def respawn_items():
    global apple, golden, poison, traps
    exclude = set(snake.body)
    apple = random_pos(exclude)
    golden = random_pos(exclude) if random.random() < 0.2 else None
    poison = random_pos(exclude) if random.random() < 0.1 else None
    traps = [random_pos(exclude) for _ in range(5)]

def draw_items():
    draw_apple(apple)
    if golden:
        pygame.draw.circle(screen, YELLOW, (golden[0] + BLOCK_SIZE // 2, golden[1] + BLOCK_SIZE // 2), 12)
    if poison:
        pygame.draw.circle(screen, (200, 50, 255), (poison[0] + BLOCK_SIZE // 2, poison[1] + BLOCK_SIZE // 2), 8)

def check_items():
    global score, speed, golden, poison, boost_timer, running
    head = snake.body[0]
    if head == apple:
        snake.grow()
        score += 1
        respawn_items()
        speed = min(25, 10 + score // 3)
    elif golden and head == golden:
        snake.grow()
        score += 5
        speed += 5
        boost_timer = time.time()
        golden = None
    elif poison and head == poison:
        running = False

def reset_game():
    global snake, score, speed, start_time, boost_timer, running
    snake = Snake()
    score = 0
    speed = 10
    boost_timer = 0
    running = True
    respawn_items()
    start_time = time.time()

def game_over_screen():
    global high_score
    if score > high_score:
        high_score = score
    screen.fill(BLACK)
    over_text = big_font.render("💀 Game Over!", True, RED)
    score_text = font.render(f"Score: {score} | High Score: {high_score}", True, WHITE)
    prompt = font.render("Press Y to play again or N to quit", True, WHITE)
    screen.blit(over_text, (WIDTH//2 - over_text.get_width()//2, HEIGHT//2 - 80))
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
    screen.blit(prompt, (WIDTH//2 - prompt.get_width()//2, HEIGHT//2 + 40))
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y: reset_game(); waiting = False
                elif event.key == pygame.K_n: pygame.quit(); exit()

def start_menu():
    screen.fill(BLACK)
    title = big_font.render("🐍 Snake Game", True, GREEN)
    click = font.render("Click Anywhere to Start", True, WHITE)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 70))
    screen.blit(click, (WIDTH//2 - click.get_width()//2, HEIGHT//2 + 10))
    pygame.display.update()

    waiting = True
    while waiting:
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); exit()
            if e.type == pygame.MOUSEBUTTONDOWN: waiting = False

# --- Game Loop ---
start_menu()
reset_game()

while True:
    while running:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); exit()
            elif event.type == pygame.KEYDOWN:
                key_map = {
                    pygame.K_UP: "UP",
                    pygame.K_DOWN: "DOWN",
                    pygame.K_LEFT: "LEFT",
                    pygame.K_RIGHT: "RIGHT"
                }
                if event.key in key_map:
                    snake.change_direction(key_map[event.key])

        snake.move()
        check_items()
        if snake.check_collision() or snake.body[0] in traps:
            running = False
            break

        if time.time() - boost_timer > 5 and speed > 10:
            speed = 10

        snake.draw()
        draw_items()
        draw_traps()

        screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))
        screen.blit(font.render(f"High Score: {high_score}", True, WHITE), (10, 40))
        screen.blit(font.render(f"Speed: {speed}", True, WHITE), (10, 70))

        pygame.display.update()
        clock.tick(speed)

    game_over_screen()
