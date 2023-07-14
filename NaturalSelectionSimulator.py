import pygame as py
import time
import math
import random
from food import Food
from creature import Creature
from Punktdiagramm import Punktdiagramm
from Histogramm import Histogramm
py.font.init()

#Konstanten und anderer Shit
WIN_WIDTH = 1400
WIN_HEIGHT = 800
PLAIN_GAP = 50
PLAIN_POSX = 50
PLAIN_POSY = 50
PLAIN_WIDTH = 900
PLAIN_HEIGHT = 600
NUM_CREATURES = 50
NUM_FOODS = 200
TIMER = 10
TIMER_FONT = py.font.SysFont("arial", 50)
run = False

def draw(win, foods, creatures, timer, nearestList, day, reproduced, died, statistics):

    #Fensterhintergrundfarbe
    win.fill((255,255,255))

    #Spielfeld
    py.draw.rect(win, (0,0,0), py.Rect(PLAIN_POSX,PLAIN_POSY,PLAIN_WIDTH,PLAIN_HEIGHT),2, 2)

    #Objekte zeichnen
    for food in foods:
        food.draw(win)
    for creature in creatures:
        creature.draw(win)
    
    #Nearestlines zeichnen
    for nearest in nearestList:
        #Schummeln Nummer 2:
        try:
            py.draw.line(win, (255,0,0),
            (creatures[nearest[0]].x_ + 0.5 * creatures[nearest[0]].width_,
            creatures[nearest[0]].y_+ 0.5 * creatures[nearest[0]].height_),
            (foods[nearest[1]].x_+ 0.5 * foods[nearest[1]].width_,
            foods[nearest[1]].y_+ 0.5 * foods[nearest[1]].height_))
        except:
            #print("fuck it")
            pass

    #Text rendern
    text = TIMER_FONT.render("Timer: " + str(timer), 1, (0,0,0))
    win.blit(text, (300, 600))
    text = TIMER_FONT.render("Day: " + str(day), 1, (0,0,0))
    win.blit(text, (600, 600))
    text = TIMER_FONT.render("Alive: " + str(len(creatures)), 1, (0,0,0))
    win.blit(text, (300, 50)) 
    text = TIMER_FONT.render("Food: " + str(len(foods)), 1, (0,0,0))
    win.blit(text, (600, 50)) 
    text = TIMER_FONT.render("Repr.: " + str(reproduced), 1, (0,0,0))
    win.blit(text, (100, 50)) 
    text = TIMER_FONT.render("Died: " + str(died), 1, (0,0,0))
    win.blit(text, (800, 50)) 

    #Statistik rendern (Alive Died Reproduced)
    for stats in statistics:
        stats.show()
    #Refresh
    py.display.update()

def run(creatures, day, reproduced, died, statistics):
    run = True
    win = py.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = py.time.Clock()
    
    #für Timer
    start = time.time()

    #Jede Runde soll neues Essen randomisiert verteilt werden
    foods = []
    for i in range(NUM_FOODS):
        foods.append(Food())

    #Reinitialisierung der Kreaturen (Rücksetzen der Energie, Status, etc.)
    for creature in creatures:
            creature.reInit()

    #"Game Loop"
    while run:
        py.display.set_caption(f"{clock.get_fps() :.1f}")
        #30 Frames pro Sekunde
        clock.tick(30)
        
        #Eventhandler
        for event in py.event.get():
            if event.type == py.QUIT:
                run = False
                py.quit()
                quit()

        #Liste, die jeder Kreatur das nächstgelegene Essen zuordnet
        nearestList = findNearest(creatures, foods)

        #bewegt Kreaturen immer zum nächstgelegenen Essen
        for nearest in nearestList:
            #hier wurde hart geschummelt:                                               Weil listenindex...
            try:
                #move1(nearest, creatures, foods)
                move2(nearest, creatures, foods)

            except:
                #print(nearest[1])
                #print(len(foods))
                pass

        #Falls kein Essen mehr auf dem Spielfeld -> Alle Kreaturen sollen zur nächstgelegenen Seite laufen
        if len(foods) == 0:
            for creature in creatures:
                if not checkSide(creature):
                    creature.updateEnergy()
                    direction = findNearestSide(creature)
                    if creature.energy_ > 0:
                        creature.move(direction)
                else:
                    creature.state_ = 3
                    creature.atHome_ = True



        #Timeraktualisierung
        timer = int(time.time()-start)
        remove = []
        moreThanOne = 0
        zero = 0
        one = 0
        two = 0
        three = 0
        if(timer >= TIMER):
            for creature in creatures:
                #Wie viele Kreaturen haben wie viele Essen gegessen
                if creature.amountIntus_ == 0:
                    zero += 1
                if creature.amountIntus_ == 1:
                    one += 1
                if creature.amountIntus_ == 2:
                    two += 1
                if creature.amountIntus_ == 3:
                    three += 1

                #mehr als 1 -> Reproduzieren, = 0 -> Tod
                if creature.amountIntus_ > 1:
                    moreThanOne += 1
                if creature.amountIntus_ == 0 or creature.atHome_ == False:
                    remove.append(creature)

            print("------------------------------------------------")
            print(f"Removed:  {len(remove)}")
            print(f"Zero: {zero}")
            print(f"One: {one}")
            print(f"Two: {two}")
            print(f"Three: {three}")
           
            
            #print(len(moreThanOne))
            #print(moreThanOne)
            run = False
            lenDied = len(remove)
            for r in remove:
                creatures.remove(r)
           # print(len(creatures))
            return (moreThanOne, lenDied)

        draw(win, foods, creatures, timer, nearestList, day, reproduced, died, statistics)
        
        
def findNearest(creatures, foods):
    nearestList = []
    for n ,c in enumerate(creatures):
        nbList = []
        for i , f in enumerate(foods):
            nbList.append(((n, i), math.sqrt((f.x_-c.x_)**2+(f.y_-c.y_)**2)))
        nbList.sort(key = lambda x: x[1])
        if(len(nbList)>0):
            nearestList.append(nbList[0][0])
    return nearestList
    
def findNearestSide(creature):
    dTop = abs(creature.y_ - PLAIN_GAP)
    dBottom = abs(PLAIN_HEIGHT+PLAIN_GAP - creature.y_)
    dLeft = abs(creature.x_ - PLAIN_GAP)
    dRight = abs(PLAIN_WIDTH+PLAIN_GAP-creature.x_)
    distance = [dTop, dBottom, dLeft, dRight]
    if dTop == min(distance):
        return (0, -1)
    if dBottom == min(distance):
        return (0, 1)
    if dLeft == min(distance):
        return (-1, 0)
    if dRight == min(distance):
        return (1, 0)

def checkSide(creature):
    if creature.x_ + creature.width_< PLAIN_GAP or creature.x_ > PLAIN_WIDTH+PLAIN_GAP or creature.y_ + creature.height_ < PLAIN_GAP or creature.y_ > PLAIN_HEIGHT+PLAIN_GAP:
        return True
    return False

def getCollision(creature, food):
    cM = creature.getMask()
    fM = food.getMask()                 

    offset = (round(food.x_) - round(creature.x_), round(food.y_) - round(creature.y_))
    collision = cM.overlap(fM, offset)
    
    if collision:
        return True
    return False


def move1(nearest, creatures, foods):
    if creatures[nearest[0]].amountIntus_ == 0 and creatures[nearest[0]].energy_ > creatures[nearest[0]].getMaxEnergy() * 0.5:
        creatures[nearest[0]].updateEnergy()
        creatures[nearest[0]].move((foods[nearest[1]].x_ - creatures[nearest[0]].x_, foods[nearest[1]].y_ - creatures[nearest[0]].y_))
    elif not checkSide(creatures[nearest[0]]):
        creatures[nearest[0]].updateEnergy()
        direction = findNearestSide(creatures[nearest[0]])
        creatures[nearest[0]].move(direction)
    elif creatures[nearest[0]].energy_ > 0:
        creatures[nearest[0]].atHome_ = True
    if getCollision(creatures[nearest[0]], foods[nearest[1]]):
        #print(f"Collision: {nearest[0]} and {nearest[1]}\n {len(foods)} {len(creatures)} {len(nearestList)}")
        #print(nearestList)
        foods.pop(nearest[1])
        creatures[nearest[0]].amountIntus_ += 1

def move2(nearest, creatures, foods):
     #Bessere Lösung nach Zustandsgraph
    #Erste Suche
    if len(foods) > 0:
        if creatures[nearest[0]].state_ == 0:
            creatures[nearest[0]].updateEnergy()
            creatures[nearest[0]].move((foods[nearest[1]].x_ - creatures[nearest[0]].x_, foods[nearest[1]].y_ - creatures[nearest[0]].y_))
            if creatures[nearest[0]].amountIntus_ == 1 and creatures[nearest[0]].energy_ > creatures[nearest[0]].getMaxEnergy() * creatures[nearest[0]].risk_:
                creatures[nearest[0]].state_ = 1
            if creatures[nearest[0]].energy_ <= creatures[nearest[0]].getMaxEnergy() * creatures[nearest[0]].risk_:
                creatures[nearest[0]].state_ = 2
        
        #Zweite Suche
        if creatures[nearest[0]].state_ == 1:
            creatures[nearest[0]].updateEnergy()
            creatures[nearest[0]].move((foods[nearest[1]].x_ - creatures[nearest[0]].x_, foods[nearest[1]].y_ - creatures[nearest[0]].y_))
            if creatures[nearest[0]].amountIntus_ == 2:
                creatures[nearest[0]].state_ = 2
            if creatures[nearest[0]].energy_ <= creatures[nearest[0]].getMaxEnergy() * creatures[nearest[0]].risk_:
                creatures[nearest[0]].state_ = 2
    
        #Heimweg
        if creatures[nearest[0]].state_ == 2:
            if not checkSide(creatures[nearest[0]]):
                creatures[nearest[0]].updateEnergy()
                direction = findNearestSide(creatures[nearest[0]])
                if creatures[nearest[0]].energy_ > 0:
                    creatures[nearest[0]].move(direction)
            else:
                creatures[nearest[0]].state_ = 3
                creatures[nearest[0]].atHome_ = True

        #Kollisionsabfrage und löschen des Essens
        if getCollision(creatures[nearest[0]], foods[nearest[1]]):
            #print(f"Collision: {nearest[0]} and {nearest[1]}\n {len(foods)} {len(creatures)} {len(nearestList)}")
            #print(nearestList)
            foods.pop(nearest[1])
            creatures[nearest[0]].amountIntus_ += 1


def main():

    #Kreaturen sollen nur ein Mal angelegt werden
    creatures = []
    alDiRe = Punktdiagramm((1100, 0), 3)
    speedHist = Histogramm((1100, 270), "Speed")
    sizeHist = Histogramm((1100, 540), "Size")
    
    died = 0
    reproduced = 0
    day = 0
    for i in range(NUM_CREATURES):
        creatures.append(Creature())
    
    while True:
        statistics = []
        day += 1
        alDiRe.update(list([(day, len(creatures), "dayAlive", 'go'), (day, died, "befDied", 'ro'), (day,reproduced, "befRepr", 'bo')]))
        speedHist.update(getSpeeds(creatures))
        sizeHist.update(getSizes(creatures))
        statistics.append(alDiRe)
        statistics.append(speedHist)
        statistics.append(sizeHist)
        addDied = run(creatures, day, reproduced, died, statistics)
        reproduced = 0
        died = 0
        for l in range(addDied[0]):
            creatures.append(Creature(*mutation()))
            reproduced += 1
        died = addDied[1]
        

def mutation():
    mutVel = 1 + zufallNeg01To01()
    mutSize = 1 + zufallNeg01To01()
    mutEff = 1 + zufallNeg01To01()
    mutRisk = 1 + zufallNeg01To01()
    return (mutVel, mutSize, 1, 1)

def zufallNeg01To01():
    return random.uniform(-0.3, 0.3)

def getSpeeds(creatures):
    speeds = []
    for creature in creatures:
        speeds.append(creature.vel_)
    return speeds

def getSizes(creatures):
    sizes = []
    for creature in creatures:
        sizes.append(creature.size_)
    return sizes

main()