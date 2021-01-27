import turtle
import random
import time
from pygame import mixer

# Registering the new shape for cannon
shape = ((0.5, 0), (0.5, 1), (1.5, 1), (1.5, 4), (-1.5, 4), (-1.5, 1), (-0.5, 1), (-0.5, 0))
turtle.register_shape('cannon', shape)

# Functions for moving cannon and bullet
def fire_bullet():
    global fire
    fire = True

def cannon_up():
    y = cannon.ycor()
    y += 20
    cannon.sety(y)

def cannon_down():
    y = cannon.ycor()
    y -= 20
    cannon.sety(y)

def game_window(wn):
    # Create a game window
    wn.title("Shooting Ball Game")
    wn.bgcolor("white")
    wn.setup(width=800, height=600)
    wn.tracer(0)
    # Keyboard inputs
    wn.listen()  # Listen for keyboard input
    wn.onkeypress(fire_bullet, "space")
    wn.onkeypress(cannon_up, "Up")
    wn.onkeypress(cannon_down, "Down")

def game_objects(balloon, cannon, bullet, message):
    # Balloon
    balloon.speed(0)
    balloon.shape("circle")
    balloon.color("green")
    balloon.shapesize(stretch_wid=2)
    balloon.penup()
    balloon.goto(-365, 0)
    # Cannon
    cannon.speed(0)
    cannon.shape("cannon")
    cannon.color("black")
    cannon.shapesize(stretch_wid=12)
    cannon.penup()
    cannon.goto(340, 0)
    # Bullet
    bullet.speed(0)
    bullet.shape("square")
    bullet.color("red")
    bullet.shapesize(stretch_wid=0.6, stretch_len=0.6)
    bullet.penup()
    bullet.goto(cannon.xcor(), cannon.ycor())
    # Message
    message.speed(0)
    message.color("red")
    message.penup()
    message.hideturtle()
    message.goto(0, 260)
    message.write("Missed Shots: 0   Game Time: 0s", align="center", font=("Comic Sans MS", 24, "normal"))

# Parameter initialization
miss = 0
fire = False
game_on = True
bullet_move = False
balloon_sd = random.choice([-1, 1]) # Random balloon moving direction
balloon_v = 0.2 # Balloon speed
balloon_vy = balloon_v * balloon_sd
bullet_vx = -0.3 # Bullet speed
time_dir = random.randint(0, 5)
game_time = 0
dir_start = time.time()
music_start = time.time()
game_start = time.time()

# Create a display window
wn = turtle.Screen()
game_window(wn)

# Create game objects, including balloon, cannon and bullet
balloon = turtle.Turtle()  # Create the balloon object
cannon = turtle.Turtle()  # Create the cannon object
bullet = turtle.Turtle()  # Create the bullet object
message = turtle.Turtle() # Create the message object
game_objects(balloon, cannon, bullet, message)

# Begin to play the Background Music
mixer.init()
mixer.music.load('BGM.mp3')
mixer.music.play()

# Main game loop
while True:
    if game_on:
        wn.update() # update the window

        # BGM play
        music_end = time.time()
        if music_end - music_start > 130:
            mixer.music.play()
            music_start = time.time()

        # Show the game time
        game_end = time.time()
        if game_end - game_start > 1:
            game_time +=1
            game_start = time.time()
            message.clear()
            message.write("Missed Shots: {}   Game Time: {}s".format(miss, game_time), align="center", font=("Comic Sans MS", 24, "normal"))

        # Hold bullet
        if bullet.xcor() < -390:
            miss += 1
            bullet.setx(cannon.xcor())
            bullet_move = False
            fire = False
            message.clear()
            message.write("Missed Shots: {}   Game Time: {}s".format(miss, game_time), align="center", font=("Comic Sans MS", 24, "normal"))
        elif bullet.xcor()== cannon.xcor():
            if fire:
                bullet_move = True
            else:
                bullet.sety(cannon.ycor())

        # Fire bullet
        if bullet_move:
            bullet.setx(bullet.xcor() + bullet_vx)

        # Randomly change the balloon moving direction
        dir_end = time.time()
        if dir_end - dir_start > time_dir:
            balloon_sd = random.choice([-1, 1])
            balloon_vy = balloon_v * balloon_sd
            dir_start = time.time()
            time_dir = random.randint(0, 5) # Random time span for changing direction
        # Move balloon
        balloon.sety(balloon.ycor() + balloon_vy)

        # Set boundaries for balloon
        if balloon.ycor() > 280:
            balloon.sety(280)
            balloon_vy *= -1
        elif balloon.ycor() < -270:
            balloon.sety(-270)
            balloon_vy *= -1
        # Set boundaries for cannon
        if cannon.ycor() > 280:
            cannon.sety(280)
        elif cannon.ycor() < -270:
            cannon.sety(-270)

        # End the game when the bullet is shot down
        if bullet.xcor() < -345 and bullet.xcor() > -355 and (bullet.ycor() < balloon.ycor() + 30 and bullet.ycor() > balloon.ycor() - 30):
            game_on = False

    else:
        # Display the number of missed shots, game time and comments for shooting performance
        if miss < 5:
            congrate = "Fantastic! You are a sharpshooter!!"
        elif miss >= 5 and miss < 10:
            congrate = "Great! You are a qualified shooter!!"
        else:
            congrate = "Not bad. You may need to practise more."
        message.setpos(0, 100)
        message.write("{}".format(congrate), align="center", font=("Comic Sans MS", 24, "normal"))