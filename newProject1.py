import turtle

def draw_face(x, y, face_color="gold"):
    t.up()
    t.goto(x, y - 50)
    t.down()
    t.color(face_color)
    t.begin_fill()
    t.circle(50)
    t.end_fill()

def draw_eyes(x, y, wink=False):
    # Left eye
    t.up()
    t.goto(x - 20, y + 20)
    t.down()
    t.color("black")
    t.begin_fill()
    t.circle(5)
    t.end_fill()

    # Right eye
    t.up()
    t.goto(x + 20, y + 20)
    t.down()
    if wink:
        t.width(3)
        t.setheading(0)
        t.forward(10)
        t.width(1)
    else:
        t.begin_fill()
        t.circle(5)
        t.end_fill()

def draw_smile(x, y):
    t.up()
    t.goto(x - 20, y - 10)
    t.setheading(-60)
    t.width(3)
    t.down()
    t.circle(20, 120)
    t.width(1)

def draw_frown(x, y):
    t.up()
    t.goto(x - 20, y - 30)
    t.setheading(60)
    t.width(3)
    t.down()
    t.circle(20, -120)
    t.width(1)

def draw_surprised_mouth(x, y):
    t.up()
    t.goto(x, y - 20)
    t.down()
    t.width(2)
    t.circle(7)

# Set up turtle
t = turtle.Turtle()
t.speed(3)

# Emoji 1: Happy face
draw_face(-180, 0)
draw_eyes(-180, 0)
draw_smile(-180, 0)

# Emoji 2: Sad face
draw_face(-60, 0)
draw_eyes(-60, 0)
draw_frown(-60, 0)

# Emoji 3: Winking face
draw_face(60, 0)
draw_eyes(60, 0, wink=True)
draw_smile(60, 0)

# Emoji 4: Surprised face
draw_face(180, 0)
draw_eyes(180, 0)
draw_surprised_mouth(180, 0)

t.hideturtle()
turtle.done()
