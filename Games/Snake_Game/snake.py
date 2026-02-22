import turtle
import time
import random

# Global variables
delay = 0.1
score = 0
high_score = 0
game_state = "menu"  # menu, playing, game_over

# Setup screen
wn = turtle.Screen()
wn.title("Snake Game by Antigravity")
wn.bgcolor("black")
wn.setup(width=600, height=600)
wn.tracer(0)  # Turns off the screen updates

# Snake head
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("white")
head.penup()
head.goto(0, 0)
head.direction = "stop"

# Snake food
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.goto(0, 100)

segments = []

# Pen for writing text
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)

# Functions
def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"

def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)

    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)

    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)

    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)

def start_easy():
    global delay, game_state
    if game_state == "menu":
        delay = 0.2
        game_state = "playing"
        reset_game_ui()

def start_medium():
    global delay, game_state
    if game_state == "menu":
        delay = 0.1
        game_state = "playing"
        reset_game_ui()

def start_hard():
    global delay, game_state
    if game_state == "menu":
        delay = 0.05
        game_state = "playing"
        reset_game_ui()

def show_menu():
    pen.clear()
    pen.goto(0, 100)
    pen.write("SNAKE GAME", align="center", font=("Courier", 36, "bold"))
    pen.goto(0, 0)
    pen.write("Press 1 for EASY", align="center", font=("Courier", 24, "normal"))
    pen.goto(0, -40)
    pen.write("Press 2 for MEDIUM", align="center", font=("Courier", 24, "normal"))
    pen.goto(0, -80)
    pen.write("Press 3 for HARD", align="center", font=("Courier", 24, "normal"))

def reset_game_ui():
    pen.clear()
    pen.goto(0, 260)
    pen.write("Score: 0  High Score: {}".format(high_score), align="center", font=("Courier", 24, "normal"))

def reset_game():
    global score, delay, game_state
    time.sleep(1)
    head.goto(0, 0)
    head.direction = "stop"

    # Hide segments
    for segment in segments:
        segment.goto(1000, 1000)
    
    segments.clear()

    score = 0
    game_state = "menu"
    show_menu()

# Keyboard bindings
wn.listen()
wn.onkeypress(go_up, "w")
wn.onkeypress(go_down, "s")
wn.onkeypress(go_left, "a")
wn.onkeypress(go_right, "d")
wn.onkeypress(go_up, "Up")
wn.onkeypress(go_down, "Down")
wn.onkeypress(go_left, "Left")
wn.onkeypress(go_right, "Right")

# Menu bindings
wn.onkeypress(start_easy, "1")
wn.onkeypress(start_medium, "2")
wn.onkeypress(start_hard, "3")

# Main Loop
show_menu()

while True:
    wn.update()

    if game_state == "playing":
        # Check for collision with the border
        if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
            reset_game()

        # Check for collision with the food
        if head.distance(food) < 20:
            # Move the food to a random spot
            x = random.randint(-290, 290)
            y = random.randint(-290, 290)
            # align to grid, roughly
            x = x - (x % 20)
            y = y - (y % 20)
            food.goto(x, y)

            # Add a segment
            new_segment = turtle.Turtle()
            new_segment.speed(0)
            new_segment.shape("square")
            new_segment.color("grey")
            new_segment.penup()
            segments.append(new_segment)

            # Increase the score
            score += 10
            if score > high_score:
                high_score = score
            
            pen.clear()
            pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))

        # Move the end segments first in reverse order
        for index in range(len(segments) - 1, 0, -1):
            x = segments[index - 1].xcor()
            y = segments[index - 1].ycor()
            segments[index].goto(x, y)

        # Move segment 0 to where the head is
        if len(segments) > 0:
            x = head.xcor()
            y = head.ycor()
            segments[0].goto(x, y)

        move()

        # Check for head collision with body segments
        for segment in segments:
            if segment.distance(head) < 20:
                reset_game()

        time.sleep(delay)
    else:
        # Just to keep the loop running without maxing CPU when in menu
        time.sleep(0.1)
