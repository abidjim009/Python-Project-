import pygame
import random
import time
import math

# Init
pygame.init()
WIDTH, HEIGHT = 800, 600
BLOCK_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🐭 Mouse Game - Cheese Hunt Edition")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont("arial", 25)
big_font = pygame.font.SysFont("impact", 60)

# Colors
WHITE = (255, 255, 255)
BLACK = (10, 10, 10)
LIGHT_GRAY = (180, 180, 180)
TRAP_GRAY = (80, 80, 80)
YELLOW = (255, 230, 100)
PINK = (255, 150, 200)
HEAD_COLOR = (200, 200, 200)

high_score = 0

def draw_mouse_block(pos, is_head=False, index=0, total=1):
    rect = pygame.Rect(*pos, BLOCK_SIZE, BLOCK_SIZE)
    shade = 200 - int(100 * (index / total))
    color = (shade, shade, shade)
    radius = 7 if is_head else 4
    pygame.draw.rect(screen, color, rect, border_radius=radius)
    if is_head:
        nose_pos = (pos[0] + BLOCK_SIZE - 4, pos[1] + BLOCK_SIZE // 2)
        pygame.draw.circle(screen, PINK, nose_pos, 3)

def draw_cheese(pos):
    # Draw cheese as a triangle
    x, y = pos[0] + BLOCK_SIZE // 2, pos[1] + BLOCK_SIZE // 2
    size = BLOCK_SIZE // 2
    points = [(x - size, y + size), (x + size, y + size), (x, y - size)]
    pygame.draw.polygon(screen, YELLOW, points)
    # Bite marks
    pygame.draw.circle(screen, BLACK, (x + 2, y), 2)
    pygame.draw.circle(screen, BLACK, (x - 2, y + 5), 2)

def draw_traps():
    for stone in traps:
        pygame.draw.rect(screen, TRAP_GRAY, (*stone, BLOCK_SIZE, BLOCK_SIZE), border_radius=2)

class Mouse:
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
            draw_mouse_block(seg, is_head=(i == 0), index=i, total=len(self.body))

    def check_collision(self):
        return self.body[0] in self.body[1:]

def random_pos(exclude=None):
    while True:
        pos = (random.randrange(0, WIDTH, BLOCK_SIZE), random.randrange(0, HEIGHT, BLOCK_SIZE))
        if not exclude or pos not in exclude:
            return pos

def respawn_items():
    global cheese, golden, poison, traps
    exclude = set(mouse.body)
    cheese = random_pos(exclude)
    golden = random_pos(exclude) if random.random() < 0.2 else None
    poison = random_pos(exclude) if random.random() < 0.1 else None
    traps = [random_pos(exclude) for _ in range(6)]

def draw_items():
    draw_cheese(cheese)
    if golden:
        pygame.draw.circle(screen, (255, 255, 0), (golden[0] + BLOCK_SIZE // 2, golden[1] + BLOCK_SIZE // 2), 14)
    if poison:
        pygame.draw.circle(screen, (180, 50, 255), (poison[0] + BLOCK_SIZE // 2, poison[1] + BLOCK_SIZE // 2), 8)

def check_items():
    global score, speed, golden, poison, boost_timer, running
    head = mouse.body[0]
    if head == cheese:
        mouse.grow()
        score += 1
        respawn_items()
        speed = min(25, 10 + score // 3)
    elif golden and head == golden:
        mouse.grow()
        score += 5
        speed += 5
        boost_timer = time.time()
        golden = None
    elif poison and head == poison:
        running = False

def reset_game():
    global mouse, score, speed, start_time, boost_timer, running
    mouse = Mouse()
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
    fade = 0
    for _ in range(30):
        fade += 8
        screen.fill((fade, fade, fade))
        pygame.display.update()
        clock.tick(30)

    screen.fill(BLACK)
    over_text = big_font.render("💀 Mouse Got Caught! 💀", True, WHITE)
    score_text = font.render(f"Score: {score} | High Score: {high_score}", True, YELLOW)
    prompt_text = font.render("Press Y to Play Again or N to Quit", True, WHITE)
    screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2 - 70))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    screen.blit(prompt_text, (WIDTH // 2 - prompt_text.get_width() // 2, HEIGHT // 2 + 40))
    pygame.display.update()

    waiting = True
    while waiting:
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_y: reset_game(); waiting = False
                elif e.key == pygame.K_n: pygame.quit(); exit()

def start_menu():
    screen.fill(BLACK)
    title = big_font.render("🐭 Cheese Hunt: Mouse Game", True, LIGHT_GRAY)
    tip = font.render("Click Anywhere to Start!", True, WHITE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 80))
    screen.blit(tip, (WIDTH // 2 - tip.get_width() // 2, HEIGHT // 2 + 10))
    pygame.display.update()

    waiting = True
    while waiting:
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); exit()
            if e.type == pygame.MOUSEBUTTONDOWN: waiting = False

# --- Game Flow ---
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
                    mouse.change_direction(key_map[event.key])

        mouse.move()
        check_items()
        if mouse.check_collision() or mouse.body[0] in traps:
            running = False
            break

        if time.time() - boost_timer > 5 and speed > 10:
            speed = 10

        mouse.draw()
        draw_items()
        draw_traps()

        # UI Info
        elapsed = int(time.time() - start_time)
        screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))
        screen.blit(font.render(f"High Score: {high_score}", True, WHITE), (10, 40))
        screen.blit(font.render(f"Time: {elapsed}s", True, WHITE), (10, 70))
        screen.blit(font.render(f"Speed: {speed}", True, WHITE), (10, 100))

        pygame.display.update()
        clock.tick(speed)

    game_over_screen()
