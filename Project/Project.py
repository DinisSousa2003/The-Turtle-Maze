#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 09:06:32 2020

@author: up202006303
"""

#setup of the general game basis, import image and sounds, create maps

import pygame, sys
pygame.init()

win_width = 600
win_height = 600

screen = pygame.display.set_mode((win_width, win_height))

pygame.display.set_caption("THE MAZE")

turtle_img = pygame.image.load("Turtle.jpg").convert()

pygame.mouse.set_visible(0)

run = True

#Game Loop

while run:
    pygame.time.delay(20)
    
    #EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #GAME LOGIC
    
    
    #DRAW
    screen.fill((0,0,0))
    pos = pygame.mouse.get_pos()
    x, y = pos
    screen.blit(turtle_img, [x,y])
    
    pygame.display.update()

pygame.quit()
sys.exit()

