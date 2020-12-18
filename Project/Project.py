#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 09:06:32 2020

@author: up202006303
"""

#setup of the general game basis, import image and sounds, create maps

import pygame, sys
pygame.init()

clock = pygame.time.Clock()

#COLORS
Green = (0, 197, 144)
Black = (0, 0, 0)
Baby_Blue = (0, 204, 255)
Golden = (255, 204, 0)

#Screen attributes
win_width = 600
win_height = 600
screen = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("THE MAZE")

#Images and Shapes
test_rect = pygame.Rect(100, 100, 100, 50) #coordinates and size
turtle_img = pygame.image.load("Turtle.jpg").convert() #turtle
pygame.mouse.set_visible(0) #mouse not visible

#Victory Text
font = pygame.font.Font('freesansbold.ttf', 28) #font file and size
text = font.render('Congrats, You are Free!!', True, Golden, Black)
textRect = text.get_rect()
textRect.center = (300, 300) # Set pos for text

#Player rect to implement collisions; arbitrary coordinates
turtle_rect = pygame.Rect(0, 0, turtle_img.get_width(), turtle_img.get_height())

run = True

#Game Loop

while run:
    
    
    clock.tick(60) #60 fps
   
    #SET BCK COLOR
    screen.fill(Baby_Blue)
   
    
    #EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #GAME LOGIC
    if turtle_rect.colliderect(test_rect):
        pygame.draw.rect(screen, Green, test_rect) #goal turns green
        screen.blit(text, textRect) # shows victory text
    else:
        pygame.draw.rect(screen, Black, test_rect) #goal is black by default
 
    
    #DRAW
    pos_mouse = pygame.mouse.get_pos()
    x_mouse, y_mouse = pos_mouse
    screen.blit(turtle_img, [x_mouse,y_mouse]) #Draw the image ate the mouse coords
    
    turtle_rect.x = x_mouse
    turtle_rect.y = y_mouse
    
    
    pygame.display.update()

pygame.quit()
sys.exit()

