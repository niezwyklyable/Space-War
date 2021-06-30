from sprite import Sprite
import math
import winsound
import random

class Player(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.8, stretch_len=1.2, outline=None)
        # zamiast speed jest dx i dy
        self.dx = 0
        self.dy = 0
        self.rotationalSpeed = 0
        
    def move(self): # nadpisanie metody move() odziedziczonej po klasie Sprite
        self.goto(self.xcor() + self.dx, self.ycor() + self.dy)
        # boundary detection
        if self.xcor() > 290:
            self.dx = - self.dx
        if self.xcor() < -290:
            self.dx = - self.dx
        if self.ycor() > 290:
            self.dy = - self.dy
        if self.ycor() < -290:
            self.dy = - self.dy

    def turn_left(self):
        self.rotationalSpeed = 30
        self.setheading(self.heading() + self.rotationalSpeed)

    def turn_right(self):
        self.rotationalSpeed = -30
        self.setheading(self.heading() + self.rotationalSpeed)

    def accelerate(self):
        self.dx += math.cos(math.radians(self.heading())) * 1 # dodaje liczbe z przedzialu <-1, 1>
        #print(self.dx)
        self.dy += math.sin(math.radians(self.heading())) * 1 # dodaje liczbe z przedzialu <-1, 1>
        #print(self.dy)

    def hyperspace(self):
        winsound.PlaySound('hyperspace.wav', winsound.SND_ASYNC)
        self.goto(random.randint(-250, 250), random.randint(-250, 250))
        