import pygame
import math
from locals import *



# ultimate

class Bullet:
    def __init__(self, pos, vector=[1,1], speed=5, mode=0):
        self.pos = pos
        self.vector = vector
        self.normalize()
        self.speed = speed
        if mode < 0 or mode >= 3:
            self.mode = 0
        else:
            self.mode = mode
        self.bullet = pygame.image.load("data/Bullet/Bullet_{}.png".format(self.mode))
        self.bullet = pygame.transform.scale(self.square, BULLET_SIZE)
        self.bullet = pygame.transform.rotate(self.bullet, -math.atan(self.vector[1]/self.vector[0]))
    
    def display(self, screen):
        screen.blit(self.bullet, self.pos)
    
    def nomalize(self): # make sure sum always equals 2
        ss = (self.vector[0]**2 + self.vector[1]**2)**0.5
        self.vector = [self.vector[0] / ss, self.vector[1]/ss]


    def move(self):
        self.pos[0] += self.vector[0] * self.speed
        self.pos[1] += self.vector[1] * self.speed
    
    def update(self, screen):
        self.move()
        self.display(screen)
        

