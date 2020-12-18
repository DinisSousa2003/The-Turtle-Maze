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
Red = (255, 0, 0)
Black = (0, 0, 0)
Baby_Blue = (0, 204, 255)

win_width = 600
win_height = 600

screen = pygame.display.set_mode((win_width, win_height))

pygame.display.set_caption("THE MAZE")

#Images and Shapes
test_rect = pygame.Rect(100, 100, 100, 50) #coordinates and size
turtle_img = pygame.image.load("Turtle.jpg").convert() #turtle
pygame.mouse.set_visible(0) #mouse not visible

#Player rect to implement collisions; arbitrary coordinates
turtle_rect = pygame.Rect(30, 30, turtle_img.get_width(), turtle_img.get_height())

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
        pygame.draw.rect(screen, Red, test_rect)
    else:
        pygame.draw.rect(screen, Black, test_rect)
 
    
    #DRAW
    pos_t = pygame.mouse.get_pos()
    x_turtle, y_turtle = pos_t
    screen.blit(turtle_img, [x_turtle,y_turtle]) #Draw the image ate the mouse coords
    
    turtle_rect.x = x_turtle
    turtle_rect.y = y_turtle
    
    
    pygame.display.update()

pygame.quit()
sys.exit()

