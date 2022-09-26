import pygame
from locals import *


class Timer:
    def __init__(self):
        self.time = 0.0
        self.font = pygame.font.SysFont("Arial", 35)
        self.text = self.font.render("Time: {:.3f}s".format(self.time), True, "WHITE")

    def display(self, screen):
        screen.blit(self.text, (WIDTH_BAR, TIMER_BAR_HEIGHT))

    def update(self, screen):
        self.display(screen)
        self.text = self.font.render("Time: {:.3f}s".format(self.time), True, "WHITE")

    def add_timer(self, time):
        self.time += time
