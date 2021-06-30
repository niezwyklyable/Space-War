import turtle
import time

class Game(): # puste nawiasy oznaczaja ze klasa Game nie dziedziczy po zadnej klasie
    def __init__(self):
        self.score = 0
        self.lives = 3
        self.level = 1
        self.status = 'playing'
        self.pen = turtle.Turtle()
        self.status_pen = turtle.Turtle()
        self.status_pen.speed(0)
        self.status_pen.color('white')
        self.status_pen.pensize(3)
        self.status_pen.penup()
        self.status_pen.ht()

    def draw_border(self):
        # draw border
        self.pen.speed(0)
        self.pen.color('white')
        self.pen.pensize(3)
        self.pen.penup()
        self.pen.goto(-300, 300)
        self.pen.pendown()
        for side in range(4):
            self.pen.fd(600)
            self.pen.rt(90)
        self.pen.penup()
        self.pen.ht()

    def show_status(self):
        if self.score <= 0:
            self.score = 0
        if self.lives <= 0:
            self.lives = 0
            self.status = 'gameover'
        self.status_pen.clear() # czysci wszystko co zostalo napisane tylko TYM dlugopisem
        if self.status == 'gameover':
            msg = 'Game Over Score: ' + str(self.score)
        else:
            msg = 'Score: ' + str(self.score) + '   Lives: ' + str(self.lives) + '   Level: ' + \
        str(self.level)
        self.status_pen.penup()
        self.status_pen.goto(-300, 310)
        self.status_pen.write(msg, font=('Arial', 16, 'normal'))

    def afterSplash(self, loop, input):
        time.sleep(5)
        turtle.bgpic('starfield.gif')
        input()
        loop() # musi byc na koncu bo petla nie konczy sie nigdy i kazda nastepna instrukcja nie jest czytana
