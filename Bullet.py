import pygame
import math
from locals import *
from lib import filename

# ultimate


class Bullet:
    def __init__(self, pos, vector=[1, 1], mode=0, speed=5, damage=1):
        self.pos = pos.copy()
        self.vector = vector.copy()
        self.normalize()
        self.speed = speed
        self.damage = damage
        self.is_hit = False
        if mode < 0 or mode >= BULLET_TYPE_NUMS:
            self.mode = 0
        else:
            self.mode = mode
        self.bullet = pygame.image.load(
            filename("Bullet/Bullet_{}.png".format(self.mode))
        )
        if mode == 0:
            self.bullet = pygame.transform.scale(self.bullet, BULLET1_SIZE)
        elif mode == 1:
            self.bullet = pygame.transform.scale(self.bullet, BULLET2_SIZE)
        if self.vector[0] > 0:
            self.angle = math.degrees(-math.atan(self.vector[1] / self.vector[0]))
        elif self.vector[0] < 0:
            self.angle = math.degrees(
                math.pi - math.atan(self.vector[1] / self.vector[0])
            )
        else:
            if self.vector[1] > 0:
                self.angle = 90
            else:
                self.angle = -90
        self.bullet = pygame.transform.rotate(self.bullet, self.angle)

    def display(self, screen):
        screen.blit(self.bullet, self.pos)

    def normalize(self):
        ss = (self.vector[0] ** 2 + self.vector[1] ** 2) ** 0.5
        self.vector = [self.vector[0] / ss, self.vector[1] / ss]

    def get_pos(self):
        return self.pos

    def move(self):
        self.pos[0] += self.vector[0] * self.speed
        self.pos[1] += self.vector[1] * self.speed

    def update(self, screen):
        self.display(screen)
        self.move()
