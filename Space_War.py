import winsound # obsluguje tylko format WAVE !!!
import random
import turtle
import time
from sprite import Sprite
from player import Player
from sprite import Enemy
from sprite import Ally
from sprite import Missile
from sprite import Particle
from sprite import Base
from sprite import Bullet
from game import Game

turtle.fd(0) # komenda inicjalizujaca okno
turtle.speed(0) # set the animations speed to the maximum
turtle.setup(700, 700) # wymiary okna x, y [px]
turtle.bgcolor('black')
turtle.bgpic('splash-screen.gif')
turtle.title('Space War by AW v1.0')
turtle.ht() # skrotowy zapis hideturtle()
#turtle.setundobuffer(1) # ustawienie pamieci w przypadku korzystania z funkcji undo()
turtle.tracer(0) # okresla co jaka liczbe klatek dokonuje sie update, ale 0 - najszybciej
turtle.register_shape('ally.gif')
turtle.register_shape('allybase.gif')
turtle.register_shape('enemy.gif')
turtle.register_shape('enemybase.gif')

# create game object
game = Game()

# draw the border
game.draw_border()

# show the game status
game.show_status()

# create my sprites
player = Player('triangle', 'white', 0, 0)
enemyBase = Base('enemybase.gif', 'red', -100, 0)
allyBase = Base('allybase.gif', 'blue', 100, 0)

missiles = []
for i in range(3):
    missiles.append(Missile('triangle', 'yellow', 0, 0))

enemies = []
enemies.append(Enemy('enemy.gif', 'red', -100, 0, random.randint(15, 345)))
# ostatni argument - zabezpieczenie przed skierowaniem wroga bezposrednio na gracza na poczatku gry

allies = []
allies.append(Ally('ally.gif', 'blue', 100, 0))

particles = []
color = ['orange', 'red', 'yellow', 'green', 'blue', 'white']

bullet = Bullet('triangle', 'red', 0, 0) # the enemy's missile

def checkIfCanFire():
    for missile in missiles:
        if missile.status == 'ready':
            return missile.fire(player)

def activateControls():
    # keyboard bindings
    turtle.listen()
    # notice: funkcje/metody trigerujemy piszac bez nawiasow !!!
    turtle.onkey(player.turn_left, 'Left')
    turtle.onkey(player.turn_right, 'Right')
    turtle.onkey(player.accelerate, 'Up')
    turtle.onkey(player.hyperspace, 'Down')
    turtle.onkey(checkIfCanFire, 'space')

def playAgain():

    ans = input('Play again? (input \'y\' if yes): ')
    if ans == 'yes' or ans == 'Yes' or ans == "YES" or ans == 'Y' or ans == 'y':

        # nie wiem o co tu chodzi...
        global allies
        global enemies
        #global game
        #global player
        global particles
        #global missiles
        #global bullet

        player.goto(0, 0)
        player.setheading(0)
        player.dx = 0
        player.dy = 0

        bullet.status = 'ready'
        
        for missile in missiles:
            missile.status = 'ready'

        for particle in particles:
            particle.ht()
        particles = []

        for enemy in enemies:
            enemy.ht()
        enemies = []
        enemies.append(Enemy('enemy.gif', 'red', -100, 0, random.randint(15, 345)))
        # ostatni argument - zabezpieczenie przed skierowaniem wroga bezposrednio na gracza na poczatku gry

        for ally in allies:
            ally.ht()
        allies = []
        allies.append(Ally('ally.gif', 'blue', 100, 0))

        game.status = 'playing'
        game.score = 0
        game.lives = 3
        game.level = 1
        game.show_status()

        return gameLoop()

    else:
        return # wyjscie z gry

# main game loop
def gameLoop():

    global particles
    counter = 0

    while True:

        turtle.update() # odmalowanie klatki - wspolpracuje z turtle.tracer(0)
        time.sleep(0.05) # delay [s] wystepujacy po kazdym odmalowaniu klatki (aby swiadomie spowolnic gre)

        player.move()
        enemyBase.move()
        allyBase.move()
        bullet.move()
        
        for missile in missiles:
            
            missile.move()

            # check for a collision between the missile and the enemy's missile (bullet) 
            if missile.is_collision(bullet, 8): # distance = 8 (domyslny argument: 20)
                winsound.PlaySound('explosion.wav', winsound.SND_ASYNC)
                missile.status = 'ready'
                # do the explosion
                for i in range(20):
                    particles.append(Particle('circle', color[random.randint(0, 5)], 0, 0))
                for particle in particles:
                    # dotyczy tylko tych particles ktore nie uczestnicza aktualnie w eksplozji
                    if particle.frame == 0:
                        particle.explode(bullet.xcor(), bullet.ycor(), 5) # range = 5 (domyslny argument: 15)
                bullet.status = 'ready'

        for enemy in enemies:

            enemy.move()

            # check for a collision between the 2 enemies
            for e in enemies:
                if enemy.is_collision(e) and e != enemy:
                    e.setheading(random.randint(0, 360))
                    e.fd(10)

            # check for a collision between the player and the enemy
            if player.is_collision(enemy):
                winsound.PlaySound('explosion.wav', winsound.SND_ASYNC) # play explosion sound
                game.score -= 100 # decrease the score
                game.lives -= 1 # decrease the lives
                game.show_status() # update the status
                # do the explosion of the player
                for i in range(20):
                    particles.append(Particle('circle', color[random.randint(0, 5)], 0, 0))
                for particle in particles:
                    # dotyczy tylko tych particles ktore nie uczestnicza aktualnie w eksplozji
                    if particle.frame == 0:
                        particle.explode(player.xcor(), player.ycor())
                player.goto(allyBase.xcor(), allyBase.ycor())
                player.setheading(random.randint(0, 360))
                player.dx = 0
                player.dy = 0
                # do the explosion of the enemy
                for i in range(20):
                    particles.append(Particle('circle', color[random.randint(0, 5)], 0, 0))
                for particle in particles:
                    # dotyczy tylko tych particles ktore nie uczestnicza aktualnie w eksplozji
                    if particle.frame == 0:
                        particle.explode(enemy.xcor(), enemy.ycor())
                enemy.goto(enemyBase.xcor(), enemyBase.ycor())
                enemy.setheading(random.randint(0, 360))
            
            # check for a collision between the ally and the enemy
            for ally in allies:
                if enemy.is_collision(ally):
                    ally.avoid()

            # check for a collision between the missile and the enemy
            for missile in missiles:
                if missile.is_collision(enemy):
                    winsound.PlaySound('explosion.wav', winsound.SND_ASYNC) # play explosion sound
                    missile.status = 'ready'
                    game.score += 100 # increase the score
                    game.show_status() # update the status
                    # do the explosion
                    for i in range(20):
                        particles.append(Particle('circle', color[random.randint(0, 5)], 0, 0))
                    for particle in particles:
                        # dotyczy tylko tych particles ktore nie uczestnicza aktualnie w eksplozji
                        if particle.frame == 0:
                            particle.explode(enemy.xcor(), enemy.ycor())
                    enemy.goto(enemyBase.xcor(), enemyBase.ycor())
                    enemy.setheading(random.randint(0, 360))

            # check for a collision between the enemy's missile (bullet) and the enemy
            if bullet.is_collision(enemy) and enemy != enemies[0]: # zawsze ten pierwszy bedzie strzelal !!!
                #print('collision index: ' + str(enemies.index(enemy)))
                winsound.PlaySound('explosion.wav', winsound.SND_ASYNC) # play explosion sound
                bullet.status = 'ready'
                # do the explosion
                for i in range(20):
                    particles.append(Particle('circle', color[random.randint(0, 5)], 0, 0))
                for particle in particles:
                    # dotyczy tylko tych particles ktore nie uczestnicza aktualnie w eksplozji
                    if particle.frame == 0:
                        particle.explode(enemy.xcor(), enemy.ycor())
                enemy.goto(enemyBase.xcor(), enemyBase.ycor())
                enemy.setheading(random.randint(0, 360))

            # oddanie strzalu przez wroga
            counter += 1 # na jedna klatke counter inkrementuje sie tyle razy ile jest wrogow
            # (im wiecej wrogow tym beda czesciej strzelac)
            if counter >= 300 and bullet.status == 'ready' and enemy == enemies[0]:
                #print(counter)
                counter = 0
                bullet.fire(enemy, player) # zawsze pierwszy enemy z listy bedzie strzelcem
                #print('fire index :' + str(enemies.index(enemy)))

        for ally in allies:

            ally.move()

            # check for a collision between the player and the ally
            if player.is_collision(ally):
                ally.avoid()

            # check for a collision between the 2 allies
            for a in allies:
                if ally.is_collision(a) and a != ally:
                    a.setheading(random.randint(0, 360))
                    a.fd(10)
                    
            # check for a collision between the missile and the ally
            for missile in missiles:
                if missile.is_collision(ally):
                    winsound.PlaySound('explosion.wav', winsound.SND_ASYNC) # play explosion sound
                    missile.status = 'ready'
                    game.score -= 50 # decrease the score
                    game.show_status() # update the status
                    # do the explosion
                    for i in range(20):
                        particles.append(Particle('circle', color[random.randint(0, 5)], 0, 0))
                    for particle in particles:
                        # dotyczy tylko tych particles ktore nie uczestnicza aktualnie w eksplozji
                        if particle.frame == 0:
                            particle.explode(ally.xcor(), ally.ycor())
                    ally.goto(allyBase.xcor(), allyBase.ycor())
                    ally.status = 'normal' # na wypadek gdyby byl w stanie 'avoid'
                    ally.setheading(random.randint(0, 360))

            # check for a collision between the enemy's missile (bullet) and the ally
            if bullet.is_collision(ally):
                winsound.PlaySound('explosion.wav', winsound.SND_ASYNC) # play explosion sound
                bullet.status = 'ready'
                # do the explosion
                for i in range(20):
                    particles.append(Particle('circle', color[random.randint(0, 5)], 0, 0))
                for particle in particles:
                    # dotyczy tylko tych particles ktore nie uczestnicza aktualnie w eksplozji
                    if particle.frame == 0:
                        particle.explode(ally.xcor(), ally.ycor())
                ally.goto(allyBase.xcor(), allyBase.ycor())
                ally.status = 'normal' # na wypadek gdyby byl w stanie 'avoid'
                ally.setheading(random.randint(0, 360))

        # check for a collision between the player and the enemy's missile (bullet)
        if bullet.is_collision(player):
            winsound.PlaySound('explosion.wav', winsound.SND_ASYNC) # play explosion sound
            bullet.status = 'ready'
            game.score -= 100 # decrease the score
            game.lives -= 1 # decrease the lives
            game.show_status() # update the status
            # do the explosion
            for i in range(20):
                particles.append(Particle('circle', color[random.randint(0, 5)], 0, 0))
            for particle in particles:
                # dotyczy tylko tych particles ktore nie uczestnicza aktualnie w eksplozji
                if particle.frame == 0:
                    particle.explode(player.xcor(), player.ycor())
            player.goto(allyBase.xcor(), allyBase.ycor())
            player.setheading(random.randint(0, 360))
            player.dx = 0
            player.dy = 0
        
        for particle in particles:
            particle.move()
            # jezeli particles zakonczyly swoje uczestnictwo w eksplozji to...
            if particle.frame == 0:
                particle.ht()
                particles.remove(particle)
        #print(len(particles))

        if game.score / game.level > 500:
            game.level += 1
            enemies.append(Enemy('enemy.gif', 'red', enemyBase.xcor(), enemyBase.ycor()))
            allies.append(Ally('ally.gif', 'blue', allyBase.xcor(), allyBase.ycor()))

        if game.status == 'gameover':
            break # wyjscie z petli ale nie z funkcji
    
    return playAgain() # wychodzac z funkcji wywolaj inna funkcje

game.afterSplash(gameLoop, activateControls) # uruchamia petle glowna gry po 5-sekundowym splash'u
# odcina tez sterowanie podczas wyswietlania splash'a (jednak nie ma to wplywu na sterowanie...)
