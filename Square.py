import random
import pygame
from locals import *


class Square:
    def __init__(self, size = [50,50], idx = -1, pos = [0,100], speed = 10, vector = [1,1]):
        if idx <= -1 or idx > 8:
            self.idx = random.randint(0, 8)  
        else:
            self.idx = idx
        self.square = pygame.image.load("data/Square/Square_{}.png".format(self.idx))
        self.square = pygame.transform.scale(self.square, (size[0], size[0]))
        self.speed = speed
        self.vector = vector
        self.nomalize()
        self.position = pos
        self.size = size
        self.point = SQUARE_POINT[self.idx]

    def nomalize(self): # make sure sum always equals 2
        ss = (self.vector[0]**2 + self.vector[1]**2)**0.5
        self.vector = [self.vector[0] / ss, self.vector[1]/ss]

    def get_point(self):
        return SQUARE_POINT[self.idx]

    def get_rect(self):
        return [self.position[0], self.position[1], self.position[0] + self.size[0], self.position[1] + self.size[1]]

    def display(self, screen):
        screen.blit(self.square, (self.position[0], self.position[1]))
        pointFont = pygame.font.SysFont("CopperPlate Gothic", 20, bold = True)  
        pointText = pointFont.render(str(self.point), True, "white")
        # screen.blit(pointText, (self.position[0] + self.size[0]/2 - 2, self.position[1] + self.size[1]/2 - 2))
        screen.blit(pointText, (self.position[0], self.position[1]))

    def update(self, screen):
        self.display(screen)
        self.position[0] += self.vector[0] * self.speed
        self.position[1] += self.vector[1] * self.speed

        # Wall
        if self.position[0] <= 0: # Left
            if self.vector[0] < 0 : self.vector[0]= -self.vector[0]
            # print("Left")
        elif self.position[0] >= WIDTH-self.size[0]: # Right
            if self.vector[0] > 0 : self.vector[0]= -self.vector[0]
            # print("Right")

        elif self.position[1] <= 0: # Top
            if self.vector[1] < 0 : self.vector[1]= -self.vector[1]
            # print("Top")

        elif self.position[1] >= HEIGHT-self.size[1]:
            if self.vector[1] > 0 : self.vector[1]= -self.vector[1]
            # print("Bottom")
        