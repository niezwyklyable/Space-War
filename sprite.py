import turtle
import random
import winsound
import math

class Sprite(turtle.Turtle): # dziedziczenie po klasie Turtle
    def __init__(self, spriteshape, color, startx, starty): # konstruktor 
        # jako pierwszy argument trzeba zdefiniowac reprezentacje instancji klasy
        # moze to byc dowolne slowo-klucz, jednak dla czytelnosci przyjelo sie stosowac "self"
        #turtle.Turtle.__init__(self, shape = spriteshape)
        turtle.Turtle.__init__(self) # dziedziczenie konstruktora
        self.shape(spriteshape)
        self.speed(0)
        self.penup()
        self.color(color)
        self.fd(0)
        self.goto(startx, starty) # odpowiednik setposition()
        self.speed = 1
    
    def move(self):
        self.fd(self.speed)
        # boundary detection
        if self.xcor() > 290:
            self.setx(290) # na wypadek gdyby obiekt przekroczyl granice z powodu zbyt duzego kroku (speed)
            self.rt(random.randint(0, 360))
        if self.xcor() < -290:
            self.setx(-290)
            self.rt(random.randint(0, 360))
        if self.ycor() > 290:
            self.sety(290)
            self.rt(random.randint(0, 360))
        if self.ycor() < -290:
            self.sety(-290)
            self.rt(random.randint(0, 360))

    def is_collision(self, other, distance = 20):
        # notice: abs nie jest czescia modulu math !!!
        if abs(self.xcor() - other.xcor()) <= distance and \
        abs(self.ycor() - other.ycor()) <= distance:
            return True
        else:
            return False

class Enemy(Sprite):
    def __init__(self, spriteshape, color, startx, starty, heading = random.randint(0, 360)):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.speed = 4
        self.setheading(heading) # domyslnie randomowy kierunek

class Ally(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.speed = 6
        self.setheading(random.randint(0, 360)) # randomowy kierunek
        self.status = 'normal'
        self.dx = 0
        self.dy = 0
        self.angle = 0
        self.centerx = 0
        self.centery = 0

    def avoid(self):
        if self.status == 'normal':
            self.status = 'avoid'
            self.centerx = self.xcor()
            self.centery = self.ycor()

    def move(self):

        if self.status == 'normal':
            self.fd(self.speed)
            self.angle = 0

        if self.status == 'avoid':
            # zatocz kolo o promieniu 10 o srodku w pkt (centerx, centery)
            self.dx = math.cos(math.radians(self.angle)) * 10 # liczba z przedzialu <-10, 10>
            self.dy = math.sin(math.radians(self.angle)) * 10 # liczba z przedzialu <-10, 10>
            self.angle += 30
            self.goto(self.centerx + self.dx, self.centery + self.dy)
            #print('x: ' + str(self.xcor()))
            #print('y: ' + str(self.ycor()))
            if self.angle >= 360:
                self.status = 'normal'

        # boundary detection
        if self.xcor() > 290:
            self.setx(290) # na wypadek gdyby obiekt przekroczyl granice z powodu zbyt duzego kroku (speed)
            self.rt(random.randint(0, 360))
        if self.xcor() < -290:
            self.setx(-290)
            self.rt(random.randint(0, 360))
        if self.ycor() > 290:
            self.sety(290)
            self.rt(random.randint(0, 360))
        if self.ycor() < -290:
            self.sety(-290)
            self.rt(random.randint(0, 360))

class Missile(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.3, stretch_len=0.4, outline=None)
        self.speed = 20
        self.status = 'ready'

    def fire(self, player):
        if self.status == 'ready':
            self.status = 'firing'
            winsound.PlaySound('laser.wav', winsound.SND_ASYNC) # play missile sound
            self.goto(player.xcor(), player.ycor())
            self.setheading(player.heading()) # ustaw pociskowi taki sam kierunek jak aktualny gracza
            
    def move(self): # nadpisanie metody move() odziedziczonej po klasie Sprite
        
        if self.status == 'ready':
            self.goto(1000, 1000)
        
        if self.status == 'firing':
            self.fd(self.speed)

        # border check
        if self.xcor() < -290 or self.xcor() > 290 or \
        self.ycor() < -290 or self.ycor() > 290:
            self.status = 'ready'

class Particle(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.goto(-1000, -1000)
        self.shapesize(stretch_wid=0.1, stretch_len=0.1, outline=None)
        self.frame = 0

    def explode(self, startx, starty, range = 15):
        self.goto(startx, starty)
        self.setheading(random.randint(0, 360))
        self.frame = 1
        self.range = range

    def move(self): # nadpisanie metody move() odziedziczonej po klasie Sprite
        
        if self.frame > 0:
            self.fd(10)
            self.frame += 1

        if self.frame > self.range:
            self.frame = 0
            self.goto(-1000, -1000)

class Base(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.speed = 2
        self.setheading(random.randint(0, 360)) # randomowy kierunek

class Bullet(Missile):
    def __init__(self, spriteshape, color, startx, starty):
        Missile.__init__(self, spriteshape, color, startx, starty)
        self.speed = 8

    def fire(self, e, p):
        if self.status == 'ready':
            self.status = 'firing'
            winsound.PlaySound('missile.wav', winsound.SND_ASYNC) # play missile sound
            self.goto(e.xcor(), e.ycor())
            # ustaw pociskowi taki kierunek aby pocisk potencjalnie trafil gracza
            if e.ycor() >= p.ycor() and e.xcor() < p.xcor():
                self.setheading(-math.degrees(math.atan(abs(e.ycor() - p.ycor()) / abs(e.xcor() - p.xcor()))))
                #print('pierwszy warunek')
            elif e.ycor() < p.ycor() and e.xcor() < p.xcor():
                self.setheading(math.degrees(math.atan(abs(e.ycor() - p.ycor()) / abs(e.xcor() - p.xcor()))))
                #print('drugi warunek')
            elif e.ycor() > p.ycor() and e.xcor() > p.xcor():
                self.setheading(180 + math.degrees(math.atan(abs(e.ycor() - p.ycor()) / abs(e.xcor() - p.xcor()))))
                #print('trzeci warunek')
            elif e.ycor() < p.ycor() and e.xcor() > p.xcor():
                self.setheading(180 - math.degrees(math.atan(abs(e.ycor() - p.ycor()) / abs(e.xcor() - p.xcor()))))
                #print('czwarty warunek')
            elif e.ycor() == p.ycor() and e.xcor() > p.xcor():
                self.setheading(180)
                #print('piaty warunek')
            elif e.ycor() > p.ycor() and e.xcor() == p.xcor():
                self.setheading(-90)
                #print('szosty warunek')
            else:
                self.setheading(90)
                #print('ostatni warunek')

    def move(self): # nadpisanie metody move() odziedziczonej po klasie Missile
        
        if self.status == 'ready':
            self.goto(-1000, 1000) # miejsce na bullet musi byc inne niz na missile
            # gdyz dochodzilo by caly czas do kollizji tych 2 obiektow
        
        if self.status == 'firing':
            self.fd(self.speed)

        # border check
        if self.xcor() < -290 or self.xcor() > 290 or \
        self.ycor() < -290 or self.ycor() > 290:
            self.status = 'ready'
            