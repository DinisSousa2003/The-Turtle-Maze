# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 19:14:35 2020

@author: User
"""

#setup of the general game basis, import image and sounds, create maps

import pygame, sys, time, random

pygame.init()

clock = pygame.time.Clock()

#COLORS
Green = (0, 197, 144)
Black = (0, 0, 0)
Baby_Blue = (0, 204, 255)
Golden = (255, 204, 0)
Red = (255, 0, 0)
White = (255, 255, 255)
Light_Grey = (211, 211, 211)
##

#Screen attributes
win_width = 600
win_height = 600
screen = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("THE TURTLE MAZE")
##

#IMAGES
turtle_img = pygame.image.load("Turtle.jpg").convert() #turtle
#Player rect to implement collisions; arbitrary coordinates
turtle_rect = pygame.Rect(0, 0, turtle_img.get_width(), turtle_img.get_height())

flipping_img = pygame.image.load("flipping turtle.jpg").convert()
history_img = pygame.image.load("History.jpg").convert()
Title_Menu = pygame.image.load("The_Turtle_Maze.png").convert()
Free_Turtle_img = pygame.image.load("Free_turtle.jpg").convert()
##

#SOUND
Death_Sound = pygame.mixer.Sound("Die Sound Effect.wav")
Button_Sound = pygame.mixer.Sound("Button.wav")
Level_Win_Sound = pygame.mixer.Sound("Level Win.wav")
Escaped_Sound = pygame.mixer.Sound("Escaped.wav")
Turtle_Inst = pygame.mixer.Sound("Turtle Instrumental.wav") #thanks Diogo Babo for the music
Go_Back_Sound = pygame.mixer.Sound("Go Back.wav")

#FILES
try:
    f1 = open("stats.txt", "r")
    f1.close()
except:
    f1 = open("stats.txt", "w")
    linhas = ["0\n","0\n","0\n","0\n","0\n","N/A\n"]
    f1.writelines(linhas)
    
    f1.close()
    
#open and readlines

def read_stats():
    f1 = open("stats.txt","r")
    linhas = f1.readlines()
    linhas = list(map(lambda x: x.strip(), linhas))
    f1.close()
    return linhas

def write_stats(linhas):
    f1 = open("stats.txt","w")
    linhas = list(map(lambda x: x + "\n", linhas))
    f1.writelines(linhas)
    f1.close()

#TILES
TILE_SIZE = 20 #(30*30)

#THE PATH OF THE GAME
def tile1(x, y):
    tile1 = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(screen, Black, tile1)
    
    
#TILES THAT APPEAT AND DISAPPEAR
def tile2(x, y, n):
    #one second is there, the other is not
    if int(time.time()) % 2 == 0: 
        tile1(x, y)
    else:
        bck(x, y, n)
 
#ENEMY PRE GAME
def tile3(x,y):
    #ENEMY
    tile3 = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE*3, TILE_SIZE*3)
    pygame.draw.rect(screen, Red, tile3) 
    
#ENEMY GAME    
def enemies(x, y):
    #ENEMY
    tile3 = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE*3, TILE_SIZE*3)
    pygame.draw.rect(screen, Red, tile3)
    
    #FIRE
    fireChance = random.random() #number 0-1
    if fireChance < Probability_of_Fire and len(bullets) <= Max_Enemy_Bullets:
        bullets.append(pygame.Rect((x*TILE_SIZE + 1.5 * TILE_SIZE, y*TILE_SIZE + Bullets_SIZE[1]), Bullets_SIZE))
    
    #BULLET CONTROL
    for b in bullets:
        
        #Move the bullets
        pygame.Rect.move_ip(b, (Vel_bullets))
        
        #Check collision
        if b.colliderect(turtle_rect):
            lost()
        
        #If bullet go off screen: remove
        if b.y < 0:
            bullets.remove(b)
        
        #Draw Bullets
        pygame.draw.rect(screen, White, b)
        

#BOLAS QUE MATAM A TESS (NÍVEL 4)
#BOLAS SUP
def draw_circles_sup(alist):
    global vel_bolas
    Radius = 5
    for i in range(len(alist)):
        #BALLS COORDS
        x, y = alist[i]
        #DRAW THE BALL
        pygame.draw.circle(screen, White, (x, y), Radius)
        #DEFINE A RECT TO HANDLE COLLISIONS
        ball = pygame.Rect((0,0), (Radius*2, Radius*2))
        #THE CENTER ARE THE COORDS
        ball.center = x, y
        
        #AS ALL BALLS COLLIDE AT THE SAME TIME, WHEN THE FIRST BALL COLLIDES
        #WITH THE WALLS ALL BALLS CHANGE THEIR DIRECTION
        if (i == 0 and (y + Radius >= 200 or y - Radius <= 140)):
            vel_bolas *= -1
        
        #SOME BALLS GO UP, OTHERS DOWN
        if x % 80 == 0:
            y += vel_bolas #coord[1] == y
        else:
            y += vel_bolas * -1
        
        #IF THE TURTLE COLLIDES WITH THE BALL
        if turtle_rect.colliderect(ball):
            lost()
        
        alist[i] = (x, y) #list are alieased so this works!
        
#BOLAS INF
def draw_circles_inf(alist, vel):
    Radius = 5
    for i in range(len(alist)):
        #BALLS COORDS
        x, y = alist[i]
        #DRAW THE BALL
        pygame.draw.circle(screen, White, (x, y), Radius)
        #DEFINE A RECT TO HANDLE COLLISIONS
        ball = pygame.Rect((0,0), (Radius*2, Radius*2))
        #THE CENTER ARE THE COORDS
        ball.center = x, y
        
        #SOME BALLS GO UP, OTHERS DOWN
        if not(x % 80 == 0):
            y += vel #coord[1] == y
        else:
            y += vel * -1
        
        #IF THE TURTLE COLLIDES WITH THE BALL
        if turtle_rect.colliderect(ball):
            lost()
       
        alist[i] = (x, y)
        
def draw_balls_pregame(list1, list2):
    Radius = 5
    for i in list1:
        #BALLS COORDS
        x, y = i
        #DRAW THE BALL
        pygame.draw.circle(screen, White, (x, y), Radius)
    for i in list2:
        #BALLS COORDS
        x, y = i
        #DRAW THE BALL
        pygame.draw.circle(screen, White, (x, y), Radius)
    
    
    
#TILE 8 IS THE GOAL CONTAINS THE WINNING CONDITION
def tile8(x, y, n):
    global level
    
    tile8 = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE*3, TILE_SIZE*2)
    if turtle_rect.colliderect(tile8) and n > 1:
        Level_Win_Sound.play()
        level += 1
        cont = pause()
        return cont
    else:
        pygame.draw.rect(screen, Green, tile8) #goal is Green by 

#TILE 9 IS THE GOAL FOR THE LAST LEVEL
def tile9(x, y, n):
    tile9 = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE*2, TILE_SIZE*3)
    if turtle_rect.colliderect(tile9) and n > 1:
           win()
    else:
        pygame.draw.rect(screen, Green, tile9) #goal is Green by default

#THE BCK (TILE 0) CONTAINS THE LOSING CONDITION
def bck(x, y, n):
    bck = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(screen, Baby_Blue, bck)
    #REMOVE TO TEST GAME WITHOUT DYING
    if turtle_rect.colliderect(bck) and n > 1:
        lost()
       

#LOSING CONDITION
def lost():
    global circles_inf, circles_sup, level, bullets
    #SET BALLS ON LEVEL 4 TO INICIAL POS
    circles_sup = [(200, 170), (240, 170), (280, 170), (320, 170), (360, 170), (400, 170), (440, 170)]
    circles_inf = [(200, 350), (240, 350), (280, 350), (320, 350), (360, 350), (400, 350), (440, 350)]
    bullets = []
    
    #INCREASE LEVEL DEATH
    linhas = read_stats()
    linhas[level] = str(int(linhas[level]) + 1)
    write_stats(linhas)
    
    #SET LEVEL TO 0
    level = 0
    
    #SET LOSING SCREEN AND BACK TO MENU
    Death_Sound.play()
    screen.fill(Baby_Blue)
    screen.blit(textLost, textLostRect)
    screen.blit(flipping_img, (100, 230))
    pygame.display.update()
    time.sleep(2.75)
    main_menu()
    
    
def win():
    global circles_inf, circles_sup, level, bullets
    #SET BALLS ON LEVEL 4 TO INICIAL POS
    circles_sup = [(200, 170), (240, 170), (280, 170), (320, 170), (360, 170), (400, 170), (440, 170)]
    circles_inf = [(200, 350), (240, 350), (280, 350), (320, 350), (360, 350), (400, 350), (440, 350)]
    bullets = []
    
    #SET LEVEL TO 0
    level = 0
    
    pygame.mixer.Sound.stop(Turtle_Inst)
    Escaped_Sound.play()
     
    screen.fill(Black)
    screen.blit(Free_Turtle_img, (25,25))
     
    #minutes and seconds passed
    t1 = round((time.time() - t0), 2)
    mn = (round(t1 // 60))
    s = round(t1 - (mn)*60)
    s = str(s) if s > 9 else ('0' + str(s))
    time_passed(mn, s)
    
    #write time stats
    time_stat = f"{mn}:{s} minutes"
    linhas = read_stats()
    linhas[5] = time_stat
    write_stats(linhas)
    
    #Win screen
    pygame.display.update()
    time.sleep(5)
    Turtle_Inst.play(-1)
    main_menu()
##        


#LEVElS

map1 = [[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	0,	0,	0,	0,	0,	1,	1,	1,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	0,	0,	0,	0,	0,	1,	1,	1,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	0,	0,	0,	0,	0,	8,	-1,	-1,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	0,	0,	0,	0,	0,	-1,	-1,	-1,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0]]


###
map2 = [[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0, 0],
[0, 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0, 0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0, 0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0, 0],
[0,	0,	0,	0,	0,	0,	0,	0,  0,	0,	0,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	0,	0,	0,	0,	0,	0, 0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	0,	0,	0,	0,	0,	0, 0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	0,	0,	0,	0,	0,	0, 0],
[0,	0,	0,	0,	0,	0,	8,	-1,	-1,	0,	0,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	0,	0,	0,	0,	0,	0, 0],
[0,	0,	0,	0,	0,	0,	-1,	-1,	-1,	0,	0,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	0,	0,	0,	0,	0,	0, 0],
[0,	0,	0,	0,	0,	0,	1,	1,	1,	0,	0,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	0,	0,	0,	0,	0,	0, 0],
[0,	0,	0,	0,	0,	0,	1,	1,	1,	0,	0,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	0,	0,	0,	0,	0,	0, 0],
[0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	1,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	0,	0,	0,	0,	0,	0, 0],
[0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	1,	1,	1,	0,	0,	1,	1,	1,	1,	1,	1,	1,	1,	0,	0,	0,	0,	0,	0, 0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	1,	1,	1,	1,	0,	0,	0,	0,	0,	0, 0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0, 0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0, 0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0, 0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0, 0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0, 0],
[0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	1,	0,	0,	0,	0,	1,	1,	1,	1,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0, 0],
[0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0, 0],
[0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0, 0],
[0,	0,	0,	0,	0,	0,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0, 0],
[0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	1,	1,	0,	0,	0,	0,	0,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0, 0],
[0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	1,	1,	0,	0,	0,	0,	0,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0, 0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	1,	1,	1,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0, 0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	1,	1,	1,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0, 0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0, 0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0, 0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0, 0]]

###
map3 = [[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	8,	-1,	-1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	-1,	-1,	-1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	1,	0,	0,	0],
[0,	0,	0,	0,	0,	1,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	1,	0,	0,	0],
[0,	0,	0,	0,	0,	1,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	1,	0,	0,	0],
[0,	0,	0,	0,	0,	1,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	2,	2,	2,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	2,	2,	2,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	2,	2,	2,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	1,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	1,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	2,	2,	2,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	1,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	2,	2,	2,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	2,	2,	2,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	2,	2,	2,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	2,	2,	2,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	2,	2,	2,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	1,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	1,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	1,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	2,	2,	2,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	2,	2,	2,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	2,	2,	2,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	1,	1,	1,	0,	0,	0,	0,	0,	0,	0,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0]]

###
map4 = [[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	0,	0,	0],
[0,	0,	0,	0,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,  1,	0,	0,	0],
[0,	0,	0,	0,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	0,	0,	0],
[0,	0,	0,	0,	0,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	0,	0,	0],
[0,	0,	0,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	0,	0,	0],
[0,	0,	0,	1,	0,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	0,	0,	0],
[0,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	1,	1,	1,	1,	1,	1,	1,	8,	-1,	-1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	1,	1,	1,	1,	1,	1,	1,	-1,	-1,	-1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,  0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0]]

circles_sup = [(200, 170), (240, 170), (280, 170), (320, 170), (360, 170), (400, 170), (440, 170)]
circles_inf = [(200, 350), (240, 350), (280, 350), (320, 350), (360, 350), (400, 350), (440, 350)]
vel_bolas = 1.1

##

#THE FINAL LEVEL HAS TILE 9 ON THE END

map5 = [[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	1,	1,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	1,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	1,	1,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	1,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	1,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	1,	1,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	1,	1,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	3,	-1,	-1,	0,	0,	0,	3,	-1,	-1,	0,	0,	0,	3,	-1,	-1,	0,	0,	1,	1,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	-1,	-1,	-1,	0,	0,	0,	-1,	-1,	-1,	0,	0,	0,	-1,	-1,	-1,	0,	0,	1,	1,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	-1,	-1,	-1,	0,	0,	0,	-1,	-1,	-1,	0,	0,	0,	-1,	-1,	-1,	0,	0,	1,	1,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	9,	-1,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	-1,	-1,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	-1,	-1,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0]]

bullets = []
Vel_bullets = (0,-1.5)
Probability_of_Fire = 0.03
Max_Enemy_Bullets = 50
Bullets_SIZE = (4, 4)

##


#LIST OF THE GAME LEVELS
list_levels = [map1, map2, map3, map4, map5] 
level = 0 #starting level

#THIS STARTING POS WHERE ACHIEVED BY TRYING AND TESTING BEST RESULTS
             	       #L1         #L2         #L3         #L4         #L5
levels_start_pos = [(292, 502), (162, 398), (483, 141), (106, 162), (462, 142)]    

## 
#Victory Text (between levels)
def vict_btlevels_DRAW(level):
    font1_1 = pygame.font.Font('freesansbold.ttf', 28) #font file and size
    textWinL = font1_1.render(f'Moving on to level {level + 1}', True, White, None)
    textWinLRect = textWinL.get_rect()
    textWinLRect.center = (300, 300) # Set pos for text
    screen.blit(textWinL, textWinLRect)
    
#Time passed to freedom
def time_passed(minutes, seconds):
    font1_1 = pygame.font.Font('freesansbold.ttf', 28) #font file and size
    textT_passed = font1_1.render(f'It took me {minutes}:{seconds} minutes to escape!', True, Black, None)
    textT_passedRect = textT_passed.get_rect()
    textT_passedRect.center = (300, 470) # Set pos for text
    screen.blit(textT_passed, textT_passedRect)


#Losing Text
font1 = pygame.font.Font('freesansbold.ttf', 28) #font file and size
textLost = font1.render("Thanks a lot... I'm back in the dungeon :(", True, Red, None)
textLostRect = textLost.get_rect()
textLostRect.center = (300, 150) # Set pos for text

#Button History Text
font2_1 = pygame.font.SysFont(None, 40)
textHistory = font2_1.render('History', True, Light_Grey, None)
textHistoryRect = textHistory.get_rect()
textHistoryRect.center = (300, 430)

#Button Play Text
# font2_1 = pygame.font.SysFont(None, 40)
textPlay = font2_1.render('Play', True, White, None)
textPlayRect = textPlay.get_rect()
textPlayRect.center = (300, 375) # Set pos for text

#Button Next Text
# font2_1 = pygame.font.SysFont(None, 40)
textNext = font2_1.render('Next', True, White, None)
textNextRect = textNext.get_rect()
textNextRect.center = (300, 350)

#Button Stats Text
# font2_1 = pygame.font.SysFont(None, 40)
textStats = font2_1.render('Stats', True, Light_Grey, None)
textStatsRect = textStats.get_rect()
textStatsRect.center = (300, 485)

#Music Text
font2_2 = pygame.font.SysFont(None, 18)
textMusic = font2_2.render("Music: The Turtles - 'Happy Together'", True, White, None)
textMusicRect = textMusic.get_rect()
textMusicRect.center = (482, 587)    

#Delete Stats Button
font2_3 = pygame.font.SysFont(None, 26)
textDelStats = font2_3.render("Reset statistics", True, White, None)
textDelStatsRect = textDelStats.get_rect()
textDelStatsRect.center = (510, 580)  

#Delete Stats Warning
font2_3 = pygame.font.SysFont(None, 26)
textStatsDeleted = font2_3.render("STATS DELETED", True, White, None)
textStatsDeletedRect = textStatsDeleted.get_rect()
textStatsDeletedRect.center = (300, 580)


#Show Stats
def Show_Stats():
    linhas = read_stats()
    
    title_font = pygame.font.SysFont(None, 75)
    
    textStats_Title= title_font.render('Statistics', True, Red, None)
    textStats_TitleRect = textStats_Title.get_rect()
    textStats_TitleRect.center= (300, 130)
    
    font2_1 = pygame.font.SysFont(None, 40)
    
    textD_Level1= font2_1.render(f'LEVEL 1: {linhas[0]} deaths', True, Light_Grey, None)
    textD_Level1Rect = textD_Level1.get_rect()
    textD_Level1Rect= (100, 200)
    
    textD_Level2= font2_1.render(f'LEVEL 2: {linhas[1]} deaths', True, White, None)
    textD_Level2Rect = textD_Level2.get_rect()
    textD_Level2Rect= (100, 250)
    
    textD_Level3= font2_1.render(f'LEVEL 3: {linhas[2]} deaths', True, Light_Grey, None)
    textD_Level3Rect = textD_Level3.get_rect()
    textD_Level3Rect= (100, 300)
    
    textD_Level4= font2_1.render(f'LEVEL 4: {linhas[3]} deaths', True, White, None)
    textD_Level4Rect = textD_Level4.get_rect()
    textD_Level4Rect = (100, 350)
    
    textD_Level5= font2_1.render(f'LEVEL 5: {linhas[4]} deaths', True, Light_Grey, None)
    textD_Level5Rect = textD_Level5.get_rect()
    textD_Level5Rect = (100, 400)
    
    textBest= font2_1.render(f'BEST TIME: {linhas[5]}', True, White, None)
    textBestRect = textBest.get_rect()
    textBestRect = (100, 450)
    
    screen.blit(textD_Level1, textD_Level1Rect)
    screen.blit(textD_Level2, textD_Level2Rect)
    screen.blit(textD_Level3, textD_Level3Rect)
    screen.blit(textD_Level4, textD_Level4Rect)
    screen.blit(textD_Level5, textD_Level5Rect)
    screen.blit(textBest, textBestRect)
    screen.blit(textStats_Title, textStats_TitleRect)
    
    
#Current Level
def C_level_DRAW(level):
    font2_3 = pygame.font.SysFont(None, 26)
    textC_level = font2_3.render(f"Level {level + 1}", True, White, None)
    textC_levelRect = textC_level.get_rect()
    textC_levelRect.center = (300, 20)
    screen.blit(textC_level, textC_levelRect)
    
#Tutorial click turtle
def Click_Turtle():    
    font2_4 = pygame.font.SysFont(None, 30)
    
    textClick_Turtle = font2_4.render("Click on the turtle", True, White, None)
    textClick_TurtleRect = textClick_Turtle.get_rect()
    textClick_TurtleRect.center = (120, 200)
    screen.blit(textClick_Turtle, textClick_TurtleRect)
        
    textClick_Turtle = font2_4.render("to begin", True, White, None)
    textClick_TurtleRect = textClick_Turtle.get_rect()
    textClick_TurtleRect.center = (120, 230)
    screen.blit(textClick_Turtle, textClick_TurtleRect)
        
def Esc_to_Exit():
     font3_1 = pygame.font.SysFont('freesans', 16)
        
     textClick_Turtle = font3_1.render("Press ESC to return", True, White, None)
     textClick_TurtleRect = textClick_Turtle.get_rect()
     textClick_TurtleRect.center = (75, 10)
     screen.blit(textClick_Turtle, textClick_TurtleRect)
        
     textClick_Turtle = font3_1.render("to the main menu", True, White, None)
     textClick_TurtleRect = textClick_Turtle.get_rect()
     textClick_TurtleRect.center = (74, 28)
     screen.blit(textClick_Turtle, textClick_TurtleRect)

# def Stats_text():
    
##

#Menu
def main_menu():
    global level, t0
    level = 0
    click = False
    while True:
        pygame.mouse.set_visible(True) #we can see the mouse on the menu
        
        clock.tick(60) #60 fps
 
        screen.fill(Black)
        
        #DRAW TEXT MENU AND BUTTONS
        screen.blit(Title_Menu, (105, 150))
        screen.blit(textPlay, textPlayRect)
        screen.blit(textHistory, textHistoryRect)
        screen.blit(textStats, textStatsRect)
        screen.blit(textMusic, textMusicRect)
 
        #Mouse Pos
        mx, my = pygame.mouse.get_pos()
        
        #CLICK PLAY
        if textPlayRect.collidepoint((mx, my)):
            if click:
                t0 = time.time()
                Button_Sound.play()
                pre_game()
        
        #CLICK HISTORY
        if textHistoryRect.collidepoint((mx, my)):
            if click:
                Button_Sound.play()
                history()
        
        #CLICK STATS
        if textStatsRect.collidepoint((mx, my)):
            if click:
                Button_Sound.play()
                stats()
        
        
        click = False
        
        #Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
 
        pygame.display.update()

##

#WHERE YOU CAN READ ABOUT TESS!
def history():
    run = True
    while run:
        clock.tick(60) #60 fps
        
        screen.fill(Black)
        
        Esc_to_Exit()
        screen.blit(history_img, (50,50))
        
        #EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Go_Back_Sound.play()
                    run = False
        
        pygame.display.update()  
##

#FIND MORE ABOUT YOUR OWN PROGRESS
def stats():
    run = True
    click = False
    while run:
        clock.tick(60) #60 fps
        
        screen.fill(Black)
        
        Esc_to_Exit()
        Show_Stats()
        screen.blit(textDelStats, textDelStatsRect)
        
        #Mouse Pos
        mx, my = pygame.mouse.get_pos()
        
        if textDelStatsRect.collidepoint((mx, my)):
            if click:
                Button_Sound.play()
                f1 = open("stats.txt", "w")
                linhas = ["0\n","0\n","0\n","0\n","0\n","N/A\n"]
                f1.writelines(linhas)
    
                f1.close()
                
                screen.blit(textStatsDeleted, textStatsDeletedRect)
                pygame.display.update()  
                time.sleep(1)
                
                
        
        click = False
        #EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Go_Back_Sound.play()
                    run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
                    
                    
        pygame.display.update()  
    

#CALLED BETWEEN LEVELS, USED WITHIN TILE8 FUNC       
def pause():
    pause = True 
    click = False
    pygame.mouse.set_visible(True)
    while pause:
            screen.fill(Baby_Blue)
            screen.blit(textNext, textNextRect)
            vict_btlevels_DRAW(level)
            
            mx, my = pygame.mouse.get_pos() 
            
            if textNextRect.collidepoint((mx, my)):
                if click:
                    Button_Sound.play()
                    pause = False
                    return True
 
            click = False
    
            #Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        Go_Back_Sound.play()
                        main_menu()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
            pygame.display.update()
##
        
#STATE PRE-GAME, YOU HAVE TO CLICK TO TURTLE TO BEGIN   
def pre_game():
    global level
    run_pre = True
    click = False
    n = 0
    while run_pre:
        clock.tick(60) #60 fps
    
        c_map = list_levels[level] #select map level
        
        #DRAW      
        y = 0
        for row in c_map:
            x = 0
            for tile in row:
                    if tile == 0:
                        bck(x, y, n)
                    if tile == 1:
                        tile1(x, y) 
                    if tile == 2:
                        tile2(x, y, n)
                    if tile == 3:
                        tile3(x, y)
                    if tile == 8:
                        if tile8(x, y, n) == True:
                            game()
                    if tile == 9:
                        tile9(x,y,n)
                    x += 1
            y += 1
        
        if level == 3:
            draw_balls_pregame(circles_sup, circles_inf)
        
        #DRAWS CURRENT LEVEL ON TOP
        C_level_DRAW(level)
        Esc_to_Exit()
        #DRAWS TUT ON LEVEL 1
        if level == 0:
            Click_Turtle()
        
        #DRAW THE TURTLE AT THE LEVEL STARTING POSITION
        #DEFINE THE RECT TO BE THERE TOO
        screen.blit(turtle_img, levels_start_pos[level])
        turtle_rect.x = levels_start_pos[level][0]
        turtle_rect.y = levels_start_pos[level][1]
        
        mx, my = pygame.mouse.get_pos()
        
        #CHECK IF TURTLE IS CLICKED
        if turtle_rect.collidepoint((mx, my)):
            if click:
                game()
        
        click = False
        
        #EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_pre = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Go_Back_Sound.play()
                    run_pre = False
                    main_menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        
        pygame.display.update()

##
        
#Game Loop
def game():
    global level, vel_bolas
    n = 0
    run = True
    
    while run:
        
        pygame.mouse.set_visible(False) #mouse not visible
        
        clock.tick(60) #60 fps
       
        c_map = list_levels[level] #select map level
       
        #DRAW      
        y = 0
        for row in c_map:
            x = 0
            for tile in row:
                if tile == 0:
                    bck(x, y, n)
                if tile == 1:
                    tile1(x, y) 
                if tile == 2:
                    tile2(x, y, n)
                if tile == 3:
                    enemies(x, y)
                if tile == 8:
                    if tile8(x, y, n) == True:
                        pre_game()
                if tile == 9:
                    tile9(x,y,n)
                x += 1
            y += 1
          
        if level == 3:
            draw_circles_sup(circles_sup)
            draw_circles_inf(circles_inf, vel_bolas)
            
        C_level_DRAW(level)
        Esc_to_Exit()
        
        #GAME LOGIC
       
        mx, my = pygame.mouse.get_pos()
        #print(mx, my) #(for control)
        screen.blit(turtle_img, [mx ,my]) #Draw the image at the mouse coords
        
        turtle_rect.x = mx
        turtle_rect.y = my
        
        
        #EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    Go_Back_Sound.play()
                    main_menu()
        
        #makes sures there are no bugs (direct wins, losses)
        if n < 2:
            n += 1 

        pygame.display.update()
       
#ACTIONS
Turtle_Inst.play(-1)
main_menu()


pygame.quit()
sys.exit()
