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

    def nomalize(self, s = 2): # make sure sum always equals 2
        self.vector[0] = self.vector[0] * s / (abs(self.vector[0]) + abs(self.vector[1]))
        self.vector[1] = self.vector[1] * s / (abs(self.vector[0]) + abs(self.vector[1]))

    def get_rect(self):
        return [self.position[0], self.position[1], self.position[0] + self.size[0], self.position[1] + self.size[1]]

    def display(self, screen):
        screen.blit(self.square, (self.position[0], self.position[1]))

    def update(self, screen):
        self.display(screen)
        self.position[0] += self.vector[0] * self.speed
        self.position[1] += self.vector[1] * self.speed
        # Corner
        med = (abs(self.vector[0]) + abs(self.vector[1]))/2
        if self.position[0] <= 0 and self.position[1] <= 0: # Top left
            self.vector = [med,med]
            print("Top left corner")
        elif self.position[0] <= 0 and self.position[1] >= HEIGHT-self.size[1]: # Bottom left
            self.vector = [-med,med]
            print("Bottom left corner")
        elif self.position[0] >= WIDTH-self.size[0] and self.position[1] <= 0: # Top right
            self.vector = [-med,med]
            print("Top right corner")
        elif self.position[0] >= WIDTH-self.size[0] and self.position[1] >= HEIGHT-self.size[1]: # Bottom right
            self.vector = [-med,-med]
            print("Bottom right corner")

        # Wall
        elif self.position[0] <= 0: # Left
            if self.vector[1] < 0:
                self.vector = [-self.vector[1], self.vector[0]]
            else:
                self.vector = [self.vector[1], -self.vector[0]]
            self.position = [self.position[0] + self.vector[0] * self.speed, self.position[1] + self.vector[1] * self.speed]
            print("Left")
        elif self.position[0] >= WIDTH-self.size[0]: # Right
            if self.vector[1] < 0:
                self.vector = [self.vector[1], -self.vector[0]]
            else:
                self.vector = [-self.vector[1], self.vector[0]]
            print("Right")
            self.position = [self.position[0] + self.vector[0] * self.speed, self.position[1] + self.vector[1] * self.speed]

        elif self.position[1] <= 0: # Top
            if self.vector[0] < 0:
                self.vector = [self.vector[1], -self.vector[0]]
            else:
                self.vector = [-self.vector[1], self.vector[0]]
            # self.vector = [self.vector[1], -self.vector[0]]
            print("Top")
            self.position = [self.position[0] + self.vector[0] * self.speed, self.position[1] + self.vector[1] * self.speed]

        elif self.position[1] >= HEIGHT-self.size[1]:
            if self.vector[0] < 0:
                self.vector = [-self.vector[1], self.vector[0]]
            else:
                self.vector = [self.vector[1], -self.vector[0]]
            print("Bottom")
            self.position = [self.position[0] + self.vector[0] * self.speed, self.position[1] + self.vector[1] * self.speed]

        