# -*- coding: utf-8 -*-
"""
@author: Denys
"""
""" It's a me, Mario! """


import pygame as pg
import numpy as np
import random
from Map_Jump_2_Mario_Jump import MakeLevel
from NN_01 import MakeNeuralNetwork

pg.init()


WIDTH = 640
HEIGHT = 640
RECTSIZE = 64
FPS = 60
TIME = 0
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()
mapsize = 9
playercolor = (255,0,0)
PLAYERSIZE = [RECTSIZE/3.0,RECTSIZE/3.0]
standing, jumping, falling, momentum = 0, 0, 0, 0

#level1colors = [('9999999'),('9532989'),('9435269'),('9382909'),('9380009'),('9114519'),('9999999')]


level1 = MakeLevel(500)
NN = MakeNeuralNetwork()


#player (y, x)
player = [(len(level1)*1.0-1.5)*RECTSIZE, 1.5*RECTSIZE]
#player = [(1.5)*RECTSIZE, 1.5*RECTSIZE]
edges = []


level1colors = list(level1)
keys = []
colors = [(0,255,0), (127,0,127), (0,0,255), (255,255,255),(255,255,255), (200,0,0),(70,173,212) , (50,50,50), (255,43,43), (0,0,0), (240,240,240), (30,30,30), (244, 241, 66)]

levelmap = pg.Surface((len(level1[0])*64, len(level1)*64))
pg.draw.rect(levelmap, (0,255,0),(0,0, len(level1)*64, len(level1[0])*64))

for y in range(len(level1)):
    for x in range(len(level1[y])):
        if int(level1[y][x]) == 1:
            pg.draw.rect(levelmap, (0,255,0), (x*RECTSIZE, y*RECTSIZE, RECTSIZE, RECTSIZE))
        else:
            pg.draw.rect(levelmap,(100,170,255), (x*RECTSIZE, y*RECTSIZE, RECTSIZE, RECTSIZE))


def move(k0, k1, k2):
    global player, standing, momentum, edges

    
    player1 = [player[0], player[1]]
    standing = 0
    if (UpdateEdges(player1[0]+1, player1[1])[1][2] == 1 or UpdateEdges(player1[0]+1, player1[1])[1][3] == 1) and (UpdateEdges(player1[0], player1[1])[1][2] != 1 and UpdateEdges(player1[0], player1[1])[1][3] != 1):
        standing = 1
        momentum = 0
        
        
    if k0 == 1:
        player1[1] -= 5
    if k1 == 1:
        player1[1] += 5
    if k2 and standing:
        momentum = -RECTSIZE/3



    if not standing:
        momentum += 1
        if momentum > RECTSIZE:
            momentum = RECTSIZE
        
    
    player1[0] += momentum        
          
    edgescore, edges = UpdateEdges(player1[0], player1[1])
    
    
    if (edges[2] == 1 or edges[3] == 1) and player1[0] > player[0]:
        newedgescore = UpdateEdges(int(player[0]/RECTSIZE +1)*RECTSIZE -PLAYERSIZE[0]/2 -1, player1[1])[0]
        if newedgescore < edgescore:
#            print "down"
            player1[0] = int(player[0]/RECTSIZE +1)*RECTSIZE -PLAYERSIZE[0]/2 -1
            edgescore = newedgescore
        
    if (edges[0] == 1 or edges[1] == 1) and player1[0] < player[0]:
        newedgescore = UpdateEdges(int(player[0]/RECTSIZE)*RECTSIZE +PLAYERSIZE[0]/2+1, player1[1])[0]
        if newedgescore < edgescore:
            player1[0] = int(player[0]/RECTSIZE)*RECTSIZE +PLAYERSIZE[0]/2 +1
            edgescore = newedgescore
            momentum = momentum / 2
#            print "up"
        
    if (edges[0] == 1 or edges[3] == 1) and player1[1] < player[1]:
        newedgescore = UpdateEdges(player1[0], int(player[1]/RECTSIZE)*RECTSIZE +PLAYERSIZE[1]/2 + 1)[0]
        if newedgescore < edgescore:
            player1[1] = int(player[1]/RECTSIZE)*RECTSIZE +PLAYERSIZE[1]/2+1
            edgescore = newedgescore
#            print "left"
        
    if (edges[1] == 1 or edges[2] == 1) and player1[1] > player[1]:
        newedgescore = UpdateEdges(player1[0], int(player[1]/RECTSIZE +1)*RECTSIZE -PLAYERSIZE[1]/2 -1)[0]
        if newedgescore < edgescore:
            player1[1] = int(player[1]/RECTSIZE +1)*RECTSIZE -PLAYERSIZE[1]/2 -1
            edgescore = newedgescore
#            print "right"
            
    if UpdateEdges(player1[0], player1[1])[0] == 0:
        player = [player1[0], player1[1]]
    
#    print player[1] / RECTSIZE / len(level1[0]) *100

        

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

    

def drawmap():
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



while TIME >= 0:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit(0)
        
    screen.fill(0)
    
    keys = pg.key.get_pressed()
    
#    wasd : 119 97 115 100
    move(keys[97],keys[100],keys[119])
    a,b = drawmap()
    drawplayer(a, b)
    
    
    TIME += 1
    pg.display.update()
    clock.tick(FPS)
    
   
#print TIME
#print player[1] / RECTSIZE / len(level1[0]) *100
pg.quit()
quit(0)
