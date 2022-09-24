import random
import pygame
import math
from locals import *


class Square(pygame.sprite.Sprite):
    def __init__(self, size=[50, 50], idx=-1, pos=[0, 100], speed=10, vector=[1, 1]):
        pygame.sprite.Sprite.__init__(self)
        if idx <= -1 or idx > 8:
            self.idx = random.randint(0, 8)
        else:
            self.idx = idx

        self.size = size
        self.origimage = pygame.image.load("data/Square/Square_{}.png".format(self.idx))
        self.origimage = pygame.transform.scale(
            self.origimage, (self.size[0], self.size[1])
        )
        self.image = self.origimage.copy()

        self.rect = self.image.get_rect(topleft=pos)
        self.speed = speed*10
        self.vector = vector
        self.normalize()
        self.position = pos
        self.point = SQUARE_POINT[self.idx]

    def normalize(self):
        ss = (self.vector[0] ** 2 + self.vector[1] ** 2) ** 0.5
        self.vector = [self.vector[0] / ss, self.vector[1] / ss]

    def get_point(self):
        return SQUARE_POINT[self.idx]

    def get_rect(self):
        return [
            self.position[0],
            self.position[1],
            self.position[0] + self.size[0],
            self.position[1] + self.size[1],
        ]

    def displayPoint(self):
        pointFont = pygame.font.SysFont("CopperPlate Gothic", int(23*self.size[0]/40), bold=True)
        pointText = pointFont.render(str(math.ceil(self.point)), True, "black")
        pointTextSize = pointFont.size(str(math.ceil(self.point)))
        self.image = self.origimage.copy()
        self.image.blit(pointText, (self.size[0]/2 - pointTextSize[0]/2, self.size[1]/2 - pointTextSize[1]/2))

    def update(self, delta):
        self.displayPoint()
        self.rect.topleft = self.position
        self.position[0] += self.vector[0] * self.speed * delta
        self.position[1] += self.vector[1] * self.speed * delta

        # Wall
        if self.position[0] <= 0 and self.vector[0] < 0:
            self.vector[0] = -self.vector[0]
        elif self.position[0] >= WIDTH - self.size[0] and self.vector[0] > 0:
            self.vector[0] = -self.vector[0]
        elif self.position[1] <= 0 and self.vector[1] < 0:
            self.vector[1] = -self.vector[1]
        elif self.position[1] >= HEIGHT - self.size[1] and self.vector[1] > 0:
            self.vector[1] = -self.vector[1]
