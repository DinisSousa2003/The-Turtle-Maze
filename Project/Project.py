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

#Screen attributes
win_width = 600
win_height = 600
screen = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("THE TURTLE MAZE")


#TILES
def tile1(x, y):
    tile1 = pygame.Rect(x*20, y*20, 20, 20)
    pygame.draw.rect(screen, Black, tile1)
    
#THE GOAL TYPE GOAL CONTAINS THE WINNING CONDITION
def tile9(x, y):
    global win
    tile9 = pygame.Rect(x*20, y*20, 40, 60)
    if turtle_rect.colliderect(tile9):
            screen.fill(Baby_Blue)
            screen.blit(textWin, textWinRect)# shows victory text
            pygame.display.update()
            time.sleep(1.5)
            main_menu()
    else:
        pygame.draw.rect(screen, Green, tile9) #goal is Green by default

#THE BCK TILE CONTAINS THE LOSING CONDITION
def bck(x, y, n):
    bck = pygame.Rect(x*20, y*20, 20, 20)
    pygame.draw.rect(screen, Baby_Blue, bck)
    if turtle_rect.colliderect(bck) and n > 1:
        screen.fill(Baby_Blue)
        screen.blit(textLost, textLostRect)
        pygame.display.update()
        time.sleep(1.5)
        main_menu()
        


#LEVEL 1
map1 = [[0, 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0, 0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0, 0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0, 0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	0,	0,	0,	0,	0,	0, 0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	0,	0,	0,	0,	0,	0, 0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	0,	0,	0,	0,	0,	0, 0],
[0,	0,	0,	0,	0,	0,	0,	9,	-1,	0,	0,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	0,	0,	0,	0,	0,	0, 0],
[0,	0,	0,	0,	0,	0,	0,	-1,	-1,	1,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	0,	0,	0,	0,	0,	0, 0],
[0,	0,	0,	0,	0,	0,	0,	-1,	-1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	0,	0,	0,	0,	0,	0, 0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	0,	0,	0,	0,	0,	0, 0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	0,	0,	0,	0,	0,	0, 0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	0,	0,	0,	0,	0,	0, 0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	1,	1,	1,	0,	0,	0,	0,	0,	0, 0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0, 0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0, 0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0, 0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0, 0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0, 0],
[0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0, 0],
[0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0, 0],
[0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0, 0],
[0,	0,	0,	0,	0,	0,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0, 0],
[0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	1,	1,	0,	0,	0,	0,	0,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0, 0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	0,	0,	0,	0,	0,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0, 0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	1,	1,	1,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0, 0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	1,	1,	1,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0, 0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0, 0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0, 0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0, 0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0, 0]]


#Images and Shapes
turtle_img = pygame.image.load("Turtle.jpg").convert() #turtle
#Player rect to implement collisions; arbitrary coordinates
turtle_rect = pygame.Rect(0, 0, turtle_img.get_width(), turtle_img.get_height())

#Victory Text
font1 = pygame.font.Font('freesansbold.ttf', 28) #font file and size
textWin = font1.render('Congrats, You are Free!!', True, White, None)
textWinRect = textWin.get_rect()
textWinRect.center = (300, 300) # Set pos for text

#Losing Text
font1 = pygame.font.Font('freesansbold.ttf', 28) #font file and size
textLost = font1.render('You failed :(((', True, Red, None)
textLostRect = textLost.get_rect()
textLostRect.center = (300, 300) # Set pos for text

#Main Menu Text
font2 = font = pygame.font.SysFont(None, 50)
textMenu = font2.render('The Turtle Maze', True, Red, Black)
textMenuRect = textMenu.get_rect()
textMenuRect.center = (300, 100) # Set pos for text

#Button Play Text
font2 = font = pygame.font.SysFont(None, 40)
textButton1 = font2.render('Play', True, White, Black)
textButton1Rect = textButton1.get_rect()
textButton1Rect.center = (161, 385) # Set pos for text


#Menu
def main_menu():
    click = False
    while True:
        pygame.mouse.set_visible(True) #we can see the mouse on the menu
        
        clock.tick(60)
 
        screen.fill(Black)
        
        #DRAW TEXT MENU AND BUTTON
        screen.blit(textMenu, textMenuRect)
        screen.blit(textButton1, textButton1Rect)
 
        #Mouse Pos
        mx, my = pygame.mouse.get_pos() 
 
        
        if textButton1Rect.collidepoint((mx, my)):
            if click:
                game()
 
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

#Game Loop
def game():
    n = 0
    run = True
    win = False
    pygame.mouse.set_visible(False) #mouse not visible
    while run:
        
        clock.tick(60) #60 fps
       
        #SET BCK COLOR
        screen.fill(Baby_Blue)
       
        #DRAW
        y = 0
        for row in map1:
            x = 0
            for tile in row:
                if tile == 0:
                    bck(x, y, n)
                if tile == 1:
                    tile1(x, y) 
                if tile == 9:
                    tile9(x, y)
                x += 1
            y += 1
        
        pos_mouse = pygame.mouse.get_pos()
        #print(pos_mouse) (for control)
        x_mouse, y_mouse = pos_mouse
        screen.blit(turtle_img, [x_mouse,y_mouse]) #Draw the image at the mouse coords
        
        turtle_rect.x = x_mouse
        turtle_rect.y = y_mouse        
       
        #GAME LOGIC
        
      
        
        #EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
     
        n += 1

        pygame.display.update()
        
        
main_menu()

pygame.quit()
sys.exit()
