import tkinter as tk
import random

# Window setup
root = tk.Tk()
root.title("Cycle Game - Multiple Obstacles")
root.resizable(False, False)

# Canvas settings
WIDTH, HEIGHT = 500, 400
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
canvas.pack()

# Player (Cycle)
cycle_width, cycle_height = 40, 40
cycle_start_x = WIDTH // 2 - cycle_width // 2
cycle_start_y = HEIGHT - cycle_height - 10
cycle = canvas.create_rectangle(cycle_start_x, cycle_start_y,
                                cycle_start_x + cycle_width,
                                cycle_start_y + cycle_height,
                                fill="green")
cycle_speed = 15

# Obstacles
obstacle_width, obstacle_height = 50, 30
obstacle_speed = 5
obstacles = []

# Game state
score = 0
move_left = move_right = False
game_running = True

# Score Display
score_text = canvas.create_text(10, 10, anchor="nw", font=("Arial", 14), text="Score: 0")

# Functions
def create_obstacle():
    x = random.randint(0, WIDTH - obstacle_width)
    return canvas.create_rectangle(x, 0, x + obstacle_width, obstacle_height, fill="red")

def move_cycle():
    if move_left:
        canvas.move(cycle, -cycle_speed, 0)
    if move_right:
        canvas.move(cycle, cycle_speed, 0)
    pos = canvas.coords(cycle)
    if pos[0] < 0:
        canvas.move(cycle, -pos[0], 0)
    if pos[2] > WIDTH:
        canvas.move(cycle, WIDTH - pos[2], 0)

def move_obstacles():
    global score, obstacle_speed, game_running
    for obstacle in obstacles:
        canvas.move(obstacle, 0, obstacle_speed)
        obs_coords = canvas.coords(obstacle)

        if obs_coords[3] > HEIGHT:
            x = random.randint(0, WIDTH - obstacle_width)
            canvas.coords(obstacle, x, 0, x + obstacle_width, obstacle_height)
            score += 1
            canvas.itemconfigure(score_text, text=f"Score: {score}")
            if score % 5 == 0:
                increase_difficulty()

        if detect_collision(obstacle):
            end_game()

def detect_collision(obstacle):
    c = canvas.coords(cycle)
    o = canvas.coords(obstacle)
    return not (c[2] < o[0] or c[0] > o[2] or c[3] < o[1] or c[1] > o[3])

def increase_difficulty():
    global obstacle_speed
    obstacle_speed += 1
    if len(obstacles) < 5:
        obstacles.append(create_obstacle())

def end_game():
    global game_running
    game_running = False
    canvas.create_text(WIDTH // 2, HEIGHT // 2, text="Game Over", fill="red", font=("Arial", 30))

def update():
    if game_running:
        move_cycle()
        move_obstacles()
        root.after(30, update)

def on_key_press(event):
    global move_left, move_right
    if event.keysym == 'Left':
        move_left = True
    elif event.keysym == 'Right':
        move_right = True

def on_key_release(event):
    global move_left, move_right
    if event.keysym == 'Left':
        move_left = False
    elif event.keysym == 'Right':
        move_right = False

# Initial setup
root.bind("<KeyPress>", on_key_press)
root.bind("<KeyRelease>", on_key_release)

# Start with 2 obstacles
obstacles.append(create_obstacle())
obstacles.append(create_obstacle())

update()
root.mainloop()
