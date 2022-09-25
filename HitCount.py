import pygame
from locals import *


class HitCount:
    def __init__(self):
        self.total = 0
        self.hit = 0
        self.font = pygame.font.SysFont("Arial", 35)
        self.totalText = self.font.render("Total: " + str(self.total), True, "WHITE")
        self.hitText = self.font.render("Hit: " + str(self.hit), True, "WHITE")

    def display(self, screen):
        screen.blit(self.totalText, (WIDTH_BAR, TOTAL_BAR_HEIGHT))
        screen.blit(self.hitText, (WIDTH_BAR, HIT_BAR_HEIGHT))

    def update(self, screen):
        self.display(screen)
        self.totalText = self.font.render("Total: " + str(self.total), True, "WHITE")
        self.hitText = self.font.render("Hit: " + str(self.hit), True, "WHITE")

    def add_total(self, total):
        self.total += total

    def add_hit(self, hit):
        self.hit += hit
