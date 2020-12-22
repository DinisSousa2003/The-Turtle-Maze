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

#LEVEL 1
goal1 = pygame.Rect(70, 70, 60, 60) #coordinates and size

#Images and Shapes
turtle_img = pygame.image.load("Turtle.jpg").convert() #turtle
#Player rect to implement collisions; arbitrary coordinates
turtle_rect = pygame.Rect(0, 0, turtle_img.get_width(), turtle_img.get_height())

#Victory Text
font1 = pygame.font.Font('freesansbold.ttf', 28) #font file and size
textWin = font1.render('Congrats, You are Free!!', True, Golden, Black)
textWinRect = textWin.get_rect()
textWinRect.center = (300, 300) # Set pos for text

#Main Menu Text
font2 = font = pygame.font.SysFont(None, 50)
textMenu = font2.render('The Turtle Maze', True, Red, Black)
textMenuRect = textMenu.get_rect()
textMenuRect.center = (300, 100) # Set pos for text

#Button 1 Text
font2 = font = pygame.font.SysFont(None, 40)
textButton1 = font2.render('Play', True, White, Black)
textButton1Rect = textButton1.get_rect()
textButton1Rect.center = (300, 300) # Set pos for text


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
       
        #WIN CONDITIOON
        if win == True:
            time.sleep(1.5)
            main_menu()
       
        #GAME LOGIC
        
        #n > 1 to avoid direct wins 
        if turtle_rect.colliderect(goal1) and n > 1:
            win = True
            pygame.draw.rect(screen, Red, goal1) #goal turns green
            screen.blit(textWin, textWinRect)# shows victory text
        else:
            pygame.draw.rect(screen, Green, goal1) #goal is Green by default
            
        
        #EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
     
        
        #DRAW
        pos_mouse = pygame.mouse.get_pos()
        x_mouse, y_mouse = pos_mouse
        screen.blit(turtle_img, [x_mouse,y_mouse]) #Draw the image ate the mouse coords
        
        turtle_rect.x = x_mouse
        turtle_rect.y = y_mouse
        
        n += 1

        pygame.display.update()
        
        
        
        
main_menu()

pygame.quit()
sys.exit()
