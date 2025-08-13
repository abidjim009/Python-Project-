import cv2
import numpy as np
import math
import mediapipe as mp
import time
from collections import deque

# Initialize Mediapipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Video capture
cap = cv2.VideoCapture(0)

# Snake parameters
snake = deque()
lengths = deque()
max_len = 150
score = 0

# Food
food_pos = [300, 300]
food_radius = 10
food_eaten = False

# Colors
snake_color = (0, 255, 0)
food_color = (0, 0, 255)

# FPS counter
prev_time = 0

def get_hand_position(frame):
    h, w, c = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            x = int(hand_landmarks.landmark[8].x * w)  # Index fingertip
            y = int(hand_landmarks.landmark[8].y * h)
            return x, y
    return None

def distance(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

def place_food():
    return [np.random.randint(50, 600), np.random.randint(50, 400)]

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    # Get fingertip position
    pos = get_hand_position(frame)

    if pos:
        snake.appendleft(pos)
        if len(snake) > 1:
            d = distance(snake[0], snake[1])
            lengths.appendleft(d)
        if sum(lengths) > max_len:
            while sum(lengths) > max_len:
                snake.pop()
                lengths.pop()

    # Draw snake
    for i in range(1, len(snake)):
        cv2.line(frame, snake[i-1], snake[i], snake_color, 10)

    # Check for food collision
    if pos and distance(pos, food_pos) < food_radius + 10:
        food_pos = place_food()
        max_len += 20
        score += 1

    # Draw food
    cv2.circle(frame, tuple(food_pos), food_radius, food_color, -1)

    # Display score
    cv2.putText(frame, f'Score: {score}', (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)

    # FPS
    cur_time = time.time()
    fps = 1 / (cur_time - prev_time) if prev_time else 0
    prev_time = cur_time
    cv2.putText(frame, f'FPS: {int(fps)}', (500, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 255, 0), 2)

    # Display
    cv2.imshow("Virtual Snake Game", frame)

    # Exit
    if cv2.waitKey(1) & 0xFF == 27:  # ESC key
        break

cap.release()
cv2.destroyAllWindows()
