# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 19:14:35 2020

@author: User
"""

#setup of the general game basis, import image and sounds, create maps

import pygame, sys, time

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
        
def tile3(x, y):
    tile3 = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(screen, Red, tile3)

#FAZER OS TILES 3, BOLAS QUE MATAM A TESS (NÍVEL 3)
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
        level += 1
        cont = pause()
        return cont
    else:
        pygame.draw.rect(screen, Green, tile8) #goal is Green by 

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
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
            pygame.display.update()


#TILE 9 IS THE GOAL FOR THE LAST LEVEL
def tile9(x, y, n):
    tile9 = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE*2, TILE_SIZE*3)
    if turtle_rect.colliderect(tile9) and n > 1:
            t1 = round((time.time() - t0), 2)
            screen.fill(Black)
            screen.blit(Free_Turtle_img, (25,25))
            #minutes and seconds passed
            mn = round(t1 // 60)
            s = round(t1 - (mn)*60)
            s = str(s) if s > 9 else ('0' + str(s))
            time_passed(mn, s)
            # screen.blit(textWin, textWinRect)# shows victory text
            pygame.display.update()
            time.sleep(5)
            main_menu()
    else:
        pygame.draw.rect(screen, Green, tile9) #goal is Green by default

#THE BCK (TILE 0) CONTAINS THE LOSING CONDITION
def bck(x, y, n):
    bck = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(screen, Baby_Blue, bck)
    #REMOVE TO TEST GAME WITHOUT DYING
    # if turtle_rect.colliderect(bck) and n > 1:
    #     lost()
       

#LOSING CONDITION
def lost():
    global circles_inf, circles_sup
    #SET BALLS ON LEVEL 2 TO INICIAL POS
    circles_sup = [(200, 170), (240, 170), (280, 170), (320, 170), (360, 170), (400, 170), (440, 170)]
    circles_inf = [(200, 350), (240, 350), (280, 350), (320, 350), (360, 350), (400, 350), (440, 350)]
    #SET LOSING SCREEN AND BACK TO MENU
    screen.fill(Baby_Blue)
    screen.blit(textLost, textLostRect)
    screen.blit(flipping_img, (100, 230))
    pygame.display.update()
    time.sleep(2.25)
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

map5 = [[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	1,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	1,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	1,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	1,	1,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	1,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	1,	1,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	1,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	1,	1,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	1,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	1,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	1,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	1,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	1,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	1,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	3,	0,	0,	0,	0,	0,	0,	0,	0,	0,	3,	0,	0,	0,	0,	0,	1,	1,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	3,	0,	0,	0,	0,	0,	0,	0,	0,	0,	3,	0,	0,	0,	0,	0,	1,	1,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	3,	3,	3,	3,	3,	0,	0,	0,	0,	0,	3,	3,	3,	3,	3,	0,	0,	0,	1,	1,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	3,	3,	3,	3,	3,	0,	0,	0,	0,	0,	3,	3,	3,	3,	3,	0,	0,	0,	1,	1,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	3,	3,	3,	3,	3,	0,	0,	0,	0,	0,	3,	3,	3,	3,	3,	0,	0,	0,	1,	1,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	9,	-1,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	-1,	-1,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	-1,	-1,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0]]

#THE FINAL LEVEL HAS TILE 9 ON THE END


#LIST OF THE GAME LEVELS
list_levels = [map1, map2, map3, map4, map5] 
level = 0 #starting level
  
#THIS STARTING POS WHERE ACHIEVED BY TRYING AND TESTING BEST RESULTS
             	       #L1         #L2         #L3         #L4         #L5
levels_start_pos = [(292, 502), (162, 398), (483, 141), (106, 162), (480, 140)]    

## 

#Victory Text
font1 = pygame.font.Font('freesansbold.ttf', 32) #font file and size
textWin = font1.render('Thanks, I am Free!!', True, Golden, None)
textWinRect = textWin.get_rect()
textWinRect.center = (300, 270) # Set pos for text

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
textHistory = font2_1.render('History', True, White, None)
textHistoryRect = textHistory.get_rect()
textHistoryRect.center = (300, 430)

#Button Play Text
font2_1 = pygame.font.SysFont(None, 40)
textPlay = font2_1.render('Play', True, White, None)
textPlayRect = textPlay.get_rect()
textPlayRect.center = (300, 485) # Set pos for text

#Button Next Text
font2_1 = pygame.font.SysFont(None, 40)
textNext = font2_1.render('Next', True, White, None)
textNextRect = textNext.get_rect()
textNextRect.center = (300, 350)

#Current Level
def C_level_DRAW(level):
    font2_2 = pygame.font.SysFont(None, 26)
    textC_level = font2_2.render(f"Level {level + 1}", True, White, None)
    textC_levelRect = textC_level.get_rect()
    textC_levelRect.center = (300, 20)
    screen.blit(textC_level, textC_levelRect)
    
#Tutorial click turtle
def Click_Turtle():    
        font2_3 = pygame.font.SysFont(None, 30)
        
        textClick_Turtle = font2_3.render("Click on the turtle", True, White, None)
        textClick_TurtleRect = textClick_Turtle.get_rect()
        textClick_TurtleRect.center = (120, 200)
        screen.blit(textClick_Turtle, textClick_TurtleRect)
        
        textClick_Turtle = font2_3.render("to begin", True, White, None)
        textClick_TurtleRect = textClick_Turtle.get_rect()
        textClick_TurtleRect.center = (120, 230)
        screen.blit(textClick_Turtle, textClick_TurtleRect)

##

#Menu
def main_menu():
    global level, t0
    level = 0
    click = False
    while True:
        pygame.mouse.set_visible(True) #we can see the mouse on the menu
        
        clock.tick(60)
 
        screen.fill(Black)
        
        #DRAW TEXT MENU AND BUTTONS
        screen.blit(Title_Menu, (105, 150))
        screen.blit(textPlay, textPlayRect)
        screen.blit(textHistory, textHistoryRect)
 
        #Mouse Pos
        mx, my = pygame.mouse.get_pos()
        
        #CLICK PLAY
        if textPlayRect.collidepoint((mx, my)):
            if click:
                t0 = time.time()
                pre_game()
        
        #CLICK HISTORY
        if textHistoryRect.collidepoint((mx, my)):
            if click:
                history()
        
        
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
        
        screen.blit(history_img, (50,50))
        
        #EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
        
        pygame.display.update()  

##
        
#STATE PRE-GAME, YOU HAVE TO CLICK TO TURTLE TO BEGIN   
def pre_game():
    global level
    run_pre = True
    click = False
    n = 0
    while run_pre:
    
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
                    tile3(x, y)
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
                    main_menu()
        
        #makes sures there are no bugs (direct wins, losses)
        if n < 2:
            n += 1 

        pygame.display.update()
        
main_menu()

pygame.quit()
sys.exit()
