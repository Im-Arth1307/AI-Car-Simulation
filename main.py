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
        
        self.center = [self.position[0] + (CAR_SIZE_X/2), self.position[1] + (CAR_SIZE_Y/2)]
        
        self.radars = []
        self.drawing_radars = []
        
        self.alive = True
        
        self.distance = 0
        self.time = 0
        
    def draw(self, screen):
        screen.blit(self.rotated_sprite, self.position)
        self.draw_radars(screen)
        
    def draw_radars(self, screen):
        for radar in self.radars:
            position = radar[0]
            pygame.draw.line(screen, (0, 255, 0), self.center, position, 1)
            pygame.draw.circle(screen, (0,2555, 0), position, 5)
            
    def check_collision(self, game_map):
        self.alive = True
        for point in self.course:
            if game_map.get_at((int(point[0]), int(point[1]))) == BORDER_COLOR:
                self.alive = False
                break
    
    