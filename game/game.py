
import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 600, 400
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cycle Game")

WHITE = (255, 255, 255)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)

clock = pygame.time.Clock()
FPS = 60

cycle_width, cycle_height = 40, 60
cycle_x = WIDTH // 2 - cycle_width // 2
cycle_y = HEIGHT - cycle_height - 10
cycle_speed = 5

obstacle_width, obstacle_height = 50, 50
obstacle_x = random.randint(0, WIDTH - obstacle_width)
obstacle_y = -obstacle_height
obstacle_speed = 5

font = pygame.font.SysFont(None, 36)

def draw_window(cycle_rect, obstacle_rect, score):
    win.fill(WHITE)
    pygame.draw.rect(win, GREEN, cycle_rect)
    pygame.draw.rect(win, RED, obstacle_rect)
    score_text = font.render(f"Score: {score}", True, BLACK)
    win.blit(score_text, (10, 10))
    pygame.display.update()

def main():
    global obstacle_speed
    running = True
    score = 0
    cycle_rect = pygame.Rect(cycle_x, cycle_y, cycle_width, cycle_height)
    obstacle_rect = pygame.Rect(obstacle_x, obstacle_y, obstacle_width, obstacle_height)

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and cycle_rect.left > 0:
            cycle_rect.x -= cycle_speed
        if keys[pygame.K_RIGHT] and cycle_rect.right < WIDTH:
            cycle_rect.x += cycle_speed

        obstacle_rect.y += obstacle_speed
        if obstacle_rect.y > HEIGHT:
            obstacle_rect.y = -obstacle_height
            obstacle_rect.x = random.randint(0, WIDTH - obstacle_width)
            score += 1
            obstacle_speed += 0.2

        if cycle_rect.colliderect(obstacle_rect):
            game_over_text = font.render("Game Over!", True, RED)
            win.blit(game_over_text, (WIDTH // 2 - 80, HEIGHT // 2 - 20))
            pygame.display.update()
            pygame.time.delay(2000)
            return

        draw_window(cycle_rect, obstacle_rect, int(score))

if __name__ == "__main__":
    main()
