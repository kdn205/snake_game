import turtle
import tkinter as tk
import time
import random
import json
from datetime import datetime
from login_panel import LoginPanel
import sys

# First, define all functions
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

def toggle_pause():
    global game_paused
    game_paused = not game_paused
    if game_paused:
        pen.clear()
        pen.write(f"PAUSED - Press P to continue\nPlayer: {player_name}  Score: {score}  High Score: {high_score}", 
                 align="center", font=("Helvetica", 24, "normal"))
    else:
        pen.clear()
        pen.write(f"Player: {player_name}  Score: {score}  High Score: {high_score}", 
                 align="center", font=("Helvetica", 24, "normal"))

def quit_game():
    # Save score before quitting if score > 0
    if score > 0:
        save_score()
    wn.bye()  # Close the turtle window
    sys.exit()  # Exit the program

def save_score():
    try:
        with open("high_scores.txt", "r") as file:
            scores = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        scores = []
    
    scores.append({
        "player": player_name,
        "score": score,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    })
    
    with open("high_scores.txt", "w") as file:
        json.dump(scores, file)

# Then initialize the game
login = LoginPanel()
player_name = login.run()

if player_name is None:
    exit()

# Initialize game variables
delay = 0.1
score = 0
high_score = 0
game_paused = False

# Set up the screen
wn = turtle.Screen()
wn.title(f"Snake Game - Player: {player_name}")
wn.bgcolor("#2C3E50")  # Dark blue background
wn.setup(width=600, height=600)
wn.tracer(0)

# Create menu bar
root = wn._root
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Create Game menu
game_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Game", menu=game_menu)
game_menu.add_command(label="Resume", command=lambda: toggle_pause() if game_paused else None)
game_menu.add_separator()
game_menu.add_command(label="Quit", command=quit_game)

# Add status bar
status_bar = turtle.Turtle()
status_bar.speed(0)
status_bar.shape("square")
status_bar.color("#ECF0F1")  # Light gray text
status_bar.penup()
status_bar.hideturtle()
status_bar.goto(0, -280)
status_bar.write("Controls: W/A/S/D - Move | P - Pause | Q - Quit", 
                align="center", font=("Helvetica", 12, "normal"))

# Add quit button
quit_button = turtle.Turtle()
quit_button.speed(0)
quit_button.shape("square")
quit_button.color("#E74C3C")  # Red color
quit_button.penup()
quit_button.goto(260, 260)
quit_button.write("Quit (Q)", align="center", font=("Helvetica", 12, "normal"))
quit_button.hideturtle()

# Initialize game objects
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("#27AE60")  # Green snake
head.penup()
head.goto(0,0)
head.direction = "stop"

# Snake food
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("#E74C3C")  # Red food
food.penup()
food.goto(0,100)

segments = []

# Pen
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("#ECF0F1")  # Light gray text
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write(f"Player: {player_name}  Score: 0  High Score: 0", align="center", font=("Helvetica", 24, "normal"))

# Keyboard bindings
wn.listen()
wn.onkeypress(go_up, "w")
wn.onkeypress(go_down, "s")
wn.onkeypress(go_left, "a")
wn.onkeypress(go_right, "d")
wn.onkey(quit_game, "q")  # Press 'q' to quit
wn.onkey(toggle_pause, "p")  # Press 'p' to pause/unpause

# Main game loop
while True:
    wn.update()
    
    if game_paused:
        continue
    
    # Check for a collision with the border
    if head.xcor()>290 or head.xcor()<-290 or head.ycor()>290 or head.ycor()<-290:
        time.sleep(1)
        head.goto(0,0)
        head.direction = "stop"
        
        # Save score before reset
        if score > 0:
            save_score()

        # Hide the segments
        for segment in segments:
            segment.goto(1000, 1000)
        
        segments.clear()
        score = 0
        delay = 0.1
        
        pen.clear()
        pen.write(f"Player: {player_name}  Score: {score}  High Score: {high_score}", 
                 align="center", font=("Helvetica", 24, "normal"))

    # Check for a collision with the food
    if head.distance(food) < 20:
        # Move the food to a random spot
        x = random.randint(-290, 290)
        y = random.randint(-290, 290)
        food.goto(x,y)

        # Add a segment
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("grey")
        new_segment.penup()
        segments.append(new_segment)

        # Shorten the delay
        delay -= 0.001

        # Increase the score
        score += 10

        if score > high_score:
            high_score = score
        
        # Update score display
        pen.clear()
        pen.write(f"Player: {player_name}  Score: {score}  High Score: {high_score}", 
                 align="center", font=("Helvetica", 24, "normal"))

    # Move the end segments first in reverse order
    for index in range(len(segments)-1, 0, -1):
        x = segments[index-1].xcor()
        y = segments[index-1].ycor()
        segments[index].goto(x, y)

    # Move segment 0 to where the head is
    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x,y)

    move()    

    # Check for head collision with the body segments
    for segment in segments:
        if segment.distance(head) < 20:
            time.sleep(1)
            head.goto(0,0)
            head.direction = "stop"
            
            # Save score before reset
            if score > 0:
                save_score()
            
            for segment in segments:
                segment.goto(1000, 1000)
            segments.clear()
            score = 0
            delay = 0.1
            
            pen.clear()
            pen.write(f"Player: {player_name}  Score: {score}  High Score: {high_score}", 
                     align="center", font=("Helvetica", 24, "normal"))

    time.sleep(delay)

wn.mainloop()