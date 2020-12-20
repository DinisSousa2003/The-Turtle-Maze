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

#Screen attributes
win_width = 600
win_height = 600
screen = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("THE MAZE")

#Images and Shapes
test_rect = pygame.Rect(100, 100, 100, 50) #coordinates and size
turtle_img = pygame.image.load("Turtle.jpg").convert() #turtle

#Victory Text
font1 = pygame.font.Font('freesansbold.ttf', 28) #font file and size
textWin = font1.render('Congrats, You are Free!!', True, Golden, Black)
textWinRect = textWin.get_rect()
textWinRect.center = (300, 300) # Set pos for text

#Main Menu Text
font2 = font = pygame.font.SysFont(None, 50)
textMenu = font2.render('Menu', True, Red, Black)
textMenuRect = textMenu.get_rect()
textMenuRect.center = (300, 100) # Set pos for text

#
click = False



#Player rect to implement collisions; arbitrary coordinates
turtle_rect = pygame.Rect(0, 0, turtle_img.get_width(), turtle_img.get_height())

#Menu
def main_menu():
    while True:
        pygame.mouse.set_visible(True) 
        
        clock.tick(60)
 
        screen.fill(Black)
        
        #main menu text here
        screen.blit(textMenu, textMenuRect)
 
        mx, my = pygame.mouse.get_pos()
 
        button_1 = pygame.Rect(280, 300, 50, 50)
        if button_1.collidepoint((mx, my)):
            if click:
                game()

        pygame.draw.rect(screen, Red, button_1)
 
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
    run = True
    pygame.mouse.set_visible(False) #mouse not visible
    while run:
        
        clock.tick(60) #60 fps
       
        #SET BCK COLOR
        screen.fill(Baby_Blue)
       
    
        #GAME LOGIC
        if turtle_rect.colliderect(test_rect):
            pygame.draw.rect(screen, Green, test_rect) #goal turns green
            screen.blit(textWin, textWinRect)# shows victory text
            
        else:
            pygame.draw.rect(screen, Black, test_rect) #goal is black by default
            
        
        #EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
     
        
        #DRAW
        pos_mouse = pygame.mouse.get_pos()
        x_mouse, y_mouse = pos_mouse
        screen.blit(turtle_img, [x_mouse,y_mouse]) #Draw the image ate the mouse coords
        
        turtle_rect.x = x_mouse
        turtle_rect.y = y_mouse
        
        
        pygame.display.update()
        
main_menu()

pygame.quit()
sys.exit()
