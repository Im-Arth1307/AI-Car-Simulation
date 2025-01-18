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
    
    def check_radar(self, degree, game_map):
        length = 0
        x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * length)
        y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * length)
        
        #While the car hasn't hit the wall
        while not game_map.get_at((x, y)) == BORDER_COLOR and length < 300:  #300 is just a max
            length += 1
            x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * length)
            y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * length)

        #Calculate the distance to the wall and append to radar list
        dist = int(math.sqrt((x - self.center[0])**2 + (y - self.center[1])**2))
        self.radars.append([(x,y) , dist])

    def update(self, game_map):
        if not self.speed_set:
            self.speed = 20
            self.speed_set = True


        #Get rotated sprite and move into the right X-direction
        #Don't let the car get closer that 20px to the edge
        self.rotated_sprite = pygame.transform.rotate(self.sprite, self.angle)
        self.position[0] += math.cos(math.radians(360 - self.angle)) * self.speed
        self.position[0] = max(self.position[0], 20)
        self.position[0] = min(self.position[0], WIDTH - 120)  #120 is the width of the car

        self.distance += self.speed
        self.time += 1

        #same for Y-direction
        self.position[1] += math.sin(math.radians(360 - self.angle)) * self.speed
        self.position[1] = max(self.position[1], 20)
        self.position[1] = min(self.position[1], WIDTH - 120)  #120 is the height of the car

        self.center = [int(self.position[0]) + CAR_SIZE_X/2, int(self.position[1]) + CAR_SIZE_Y/2]

        # Calculate Four Corners
        # Length Is Half The Side
        length = 0.5 * CAR_SIZE_X
        left_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 30))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 30))) * length]
        right_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 150))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 150))) * length]
        left_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 210))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 210))) * length]
        right_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 330))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 330))) * length]
        self.corners = [left_top, right_top, left_bottom, right_bottom]

        # Check Collisions And Clear Radars
        self.check_collision(game_map)
        self.radars.clear()

        # From -90 To 120 With Step-Size 45 Check Radar
        for d in range(-90, 120, 45):
            self.check_radar(d, game_map)


    