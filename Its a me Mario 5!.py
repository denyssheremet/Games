# -*- coding: utf-8 -*-
"""
Simpler NN
for playing Mario Jump
"""
""" It's a me, Mario! """
    
    
import pygame as pg
import numpy as np
import random
import math
import sys
from Map_Jump_2_Mario_Jump import MakeLevel
#from NN_03 import MakeNN

pg.init()
    
""" variables for game """
WIDTH = 640
HEIGHT = 640
RECTSIZE = 64
FPS = 60
    
""" variables for NN """
IN, h0, OUT = 42, 4, 1
NODEAMOUNTS = [IN, h0, OUT]

scores = []
goal = [0,1,1]

amountNN = 100
nodes = np.array([[0.0]*IN, [0.0]*h0, [0.0]*OUT])
lines = np.array(np.zeros((amountNN,2,IN*h0)))


""" Neural network functions """
def InitiateNodes(IN, h0, OUT):
    for i in range(IN):
        nodes[0][i] = float(random.randint(0,1)*2 - 1)


def InitiateLines():
    global lines
    for NN in range(amountNN):
        for i in range(len(lines[NN])):
            for a in range(NODEAMOUNTS[i]*NODEAMOUNTS[i+1]):
                rand = random.uniform(-100,100)
#                rand = random.randint(-10,10)
                lines[NN,i,a] = rand


def sigmoid(x):
  return 2 / (1 + math.exp(-x)) -1
    

def CalculateSections(NN, INPUT):
    for a in range(h0):
        nodes[1][a] = int(round(sigmoid(sum(INPUT * lines[NN][0][a*IN:(a+1)*IN]))))
    for a in range(OUT):
        nodes[2][a] = int(round(sigmoid(sum(nodes[1] * lines[NN][1][a*h0:(a+1)*h0]))))
        
    return list(nodes[2])


def Mutate(lineslist1):
    lineslist2 = np.copy(lineslist1)
    for y in range(len(lineslist1)):
        for x in range(NODEAMOUNTS[y]*NODEAMOUNTS[y+1]):
            randnumber = random.randint(0,1)

            if not randnumber:
                lineslist2[y][x] += random.uniform(-20,20)

    return lineslist2
        

        

def BestOfGeneration(amount):
    scores1, lines1 = list(scores), list(lines)
    bestscores, bestlines = [], []
    for i in range(amount):
        if len(scores1):
            mincost = min(scores1)
            bestlines.append(lines1.pop(scores1.index(mincost)))
            bestscores.append(scores1.pop(scores1.index(mincost)))
    return list(bestscores), list(bestlines)


def FirstRound( survivors, playingtime ):
    global scores, lines
    for NN in range( amountNN ):
        cost = gameloop( lines[NN], NN, playingtime, 0 )
        scores.append(cost)
        print (NN)
    scores, lines = BestOfGeneration(survivors)
    gameloop(lines[0], 0, 300, 1)


def GenerationRound(rounds, mutations, survivors, playingtime, showrun=0):
    global scores, lines
    for iteration in range(rounds):
        for NN in range(len(lines)):

            for i in range(mutations):
                l1 = Mutate(list(lines[NN]))
                lines = np.concatenate((lines, [l1]))
                
                cost = gameloop( lines[len(lines) - 1], len(lines) - 1, playingtime, 0 )
                scores.append(cost)

        scores, lines = BestOfGeneration(survivors)  
        if showrun:
            gameloop(lines[0], 0, 300, 1)


    
""" Game """   
def gameloop( NN , NNnumber, playingtime, visual):    
    TIME = 0
    if visual:
        screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    playercolor = (255,0,0)
    PLAYERSIZE = [RECTSIZE/3.0,RECTSIZE/3.0]
    standing, jumping, falling, momentum = 0, 0, 0, 0
    
    
    level1 = MakeLevel(50)
    
    
    Player = [(len(level1)*1.0-1.5)*RECTSIZE, 7.5*RECTSIZE]
    edges = []
    
    keys = []
    
    levelmap = pg.Surface((len(level1[0])*RECTSIZE, len(level1)*RECTSIZE))
    pg.draw.rect(levelmap, (0,255,0),(0,0, len(level1)*RECTSIZE, len(level1[0])*RECTSIZE))
    
    for y in range(len(level1)):
        for x in range(len(level1[y])):
            if int(level1[y][x]) == 1:
                pg.draw.rect(levelmap, (0,255,0), (x*RECTSIZE, y*RECTSIZE, RECTSIZE, RECTSIZE))
            else:
                pg.draw.rect(levelmap,(100,170,255), (x*RECTSIZE, y*RECTSIZE, RECTSIZE, RECTSIZE))
    
    
    def move(k0, k1, player, standing, momentum, edges):
     
        player1 = [player[0], player[1]]
        standing = 0
        if (UpdateEdges(player1[0]+1, player1[1])[1][2] == 1 or UpdateEdges(player1[0]+1, player1[1])[1][3] == 1) and (UpdateEdges(player1[0], player1[1])[1][2] != 1 and UpdateEdges(player1[0], player1[1])[1][3] != 1):
            standing = 1
            momentum = 0
            
        if k0 == 1:
            player1[1] -= 5
        if k0 == -1:
            player1[1] += 5
        if k1 and standing:
            momentum = -RECTSIZE/8.0*2.5
    
    
    
        if not standing:
            momentum += 1
            if momentum > RECTSIZE:
                momentum = RECTSIZE
            
        
        player1[0] += momentum        
              
        edgescore, edges = UpdateEdges(player1[0], player1[1])
        
        
        if (edges[2] == 1 or edges[3] == 1) and player1[0] > player[0]:
            newedgescore = UpdateEdges(int(player[0]/RECTSIZE +1)*RECTSIZE -PLAYERSIZE[0]/2 -1, player1[1])[0]
            if newedgescore < edgescore:
                player1[0] = int(player[0]/RECTSIZE +1)*RECTSIZE -PLAYERSIZE[0]/2 -1
                edgescore = newedgescore
            
        if (edges[0] == 1 or edges[1] == 1) and player1[0] < player[0]:
            newedgescore = UpdateEdges(int(player[0]/RECTSIZE)*RECTSIZE +PLAYERSIZE[0]/2+1, player1[1])[0]
            if newedgescore < edgescore:
                player1[0] = int(player[0]/RECTSIZE)*RECTSIZE +PLAYERSIZE[0]/2 +1
                edgescore = newedgescore
                momentum = momentum / 2
            
        if (edges[0] == 1 or edges[3] == 1) and player1[1] < player[1]:
            newedgescore = UpdateEdges(player1[0], int(player[1]/RECTSIZE)*RECTSIZE +PLAYERSIZE[1]/2 + 1)[0]
            if newedgescore < edgescore:
                player1[1] = int(player[1]/RECTSIZE)*RECTSIZE +PLAYERSIZE[1]/2+1
                edgescore = newedgescore
            
        if (edges[1] == 1 or edges[2] == 1) and player1[1] > player[1]:
            newedgescore = UpdateEdges(player1[0], int(player[1]/RECTSIZE +1)*RECTSIZE -PLAYERSIZE[1]/2 -1)[0]
            if newedgescore < edgescore:
                player1[1] = int(player[1]/RECTSIZE +1)*RECTSIZE -PLAYERSIZE[1]/2 -1
                edgescore = newedgescore
                
        if UpdateEdges(player1[0], player1[1])[0] == 0:
            player = [player1[0], player1[1]]
        
        return player, standing, momentum, edges
    
            
    
    def UpdateEdges(y1, x1):
    #    global edges
        edges = [0,0,0,0]
        if int(level1[int((y1+PLAYERSIZE[0]/2)/RECTSIZE)][int((x1+PLAYERSIZE[1]/2)/RECTSIZE)]) == 1:
            edges[2] = 1
        if int(level1[int((y1+PLAYERSIZE[0]/2)/RECTSIZE)][int((x1-PLAYERSIZE[1]/2)/RECTSIZE)]) == 1:
            edges[3] = 1
        if int(level1[int((y1-PLAYERSIZE[0]/2)/RECTSIZE)][int((x1+PLAYERSIZE[1]/2)/RECTSIZE)]) == 1:
            edges[1] = 1
        if int(level1[int((y1-PLAYERSIZE[0]/2)/RECTSIZE)][int((x1-PLAYERSIZE[1]/2)/RECTSIZE)]) == 1:
            edges[0] = 1 
        
        edgescore = 0
        for e in edges:
            edgescore += e
        return edgescore, edges
    
        
    
    def drawmap(player):
        a, b, xm, ym = 0, 0, WIDTH/2-int(player[1]), HEIGHT/2-int(player[0])
        if WIDTH/2-int(player[1]) > 0:
            xm = 0
            a = -WIDTH/2+int(player[1])
        elif WIDTH/2-int(player[1]) + len(level1[0])*RECTSIZE < WIDTH:
            xm = WIDTH - (len(level1[0])*RECTSIZE)
            a = WIDTH/2 - len(level1[0])*RECTSIZE + int(player[1])  
        if HEIGHT/2-int(player[0]) > 0:
            ym = 0
            b = -HEIGHT/2+int(player[0])
        elif WIDTH/2-int(player[0]) + len(level1)*RECTSIZE < HEIGHT:
            ym = HEIGHT - (len(level1)*RECTSIZE)
            b = HEIGHT/2 - len(level1)*RECTSIZE + int(player[0])  
    
        screen.blit(levelmap, (xm, ym))
        return a,b
    
    
    
    def drawplayer(x,y):
        pg.draw.circle(screen, playercolor, (int(WIDTH/2 + x), int(HEIGHT/2 + y)), int(RECTSIZE/6.0))
    
    
    def Input(player):
        py = int(player[0]/RECTSIZE)
        px = int(player[1]/RECTSIZE)
        INPUT = []
        for y in range(6):
            for x in range(7):
                if py + y - 3 >= 0 and px + x-3 >= 0:
                    try:
                        INPUT.append(int(level1[py + y - 3][px + x-3]))
                    except IndexError:
                        INPUT.append(0)
                else:
                    INPUT.append(0)
        return INPUT
    
    
    while TIME < playingtime + 60:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit(0)
        if visual:  
            screen.fill(0)

        INPUT = Input(Player)
        if TIME < playingtime:
            key = CalculateSections(NNnumber, INPUT)
            Player, standing, momentum, edges = move(key[0], 1, Player, standing, momentum, edges)
        else:
            Player, standing, momentum, edges = move(0, 0, Player, standing, momentum, edges)
        
        
        if visual:
            a,b = drawmap(Player)
            drawplayer(a, b)
        
        
        TIME += 1
        if visual:
            pg.display.update()
            clock.tick(FPS)
       
    return Player[0] / RECTSIZE #/ len(level1)

def saveResult( tofile, result ):
    f = open(tofile, 'w')
    sys.stdout = f
    for line in result:
        for e in line:
            continue
    f.close()


""" Evolution """
InitiateNodes(IN, h0, OUT)
InitiateLines()

FirstRound(10, 600)


GenerationRound(10, 40, 10, 1200, 1)

GenerationRound(10, 20, 10, 2400, 1)
saveResult("test.txt", lines[0])

GenerationRound(15, 10, 10, 3600,1)
saveResult("test.txt", lines[0])

GenerationRound(20, 10, 10, 1500)
saveResult("test.txt", lines[0])

GenerationRound(20, 20, 5, 1800)

GenerationRound(20, 10, 10, 2400)

pg.quit()
quit(0)