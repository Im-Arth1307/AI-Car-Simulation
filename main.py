import os
import sys
import math
import random
import neat
import pygame

WIDTH  =1600
HEIGHT =880

CAR_SIZE_X = 60
CAR_SIZE_Y = 60

BORDER_COLOR = (255, 255, 255, 255) # Color To Crash on Hit

current_generation = 0

class Car:
    def __init__(self):
        self.sprite = pygame.image.load("car.png").convert()
        self.sprite = pygame.transform.scale(self.sprite, (CAR_SIZE_X, CAR_SIZE_Y))
        self.rotated_sprite = self.sprite
        
        self.position = [830, 920]
        self.angle = 0
        self.speed = 0
        
        self.speed_set = False
        
        self.center = [self.position[0]]