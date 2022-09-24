import pygame
from locals import *

class Score:
    def __init__(self):
        self.score = 0
        self.font = pygame.font.SysFont("Arial", 35)
        self.text = self.font.render("Score: " + str(self.score), True, "WHITE")
    
    def display(self, screen):
        screen.blit(self.text, (BAR_HEIGHT, BAR_HEIGHT))
    
    def update(self, screen):
        self.display(screen)
        self.text = self.font.render("Score: " + str(self.score), True, "WHITE")
    
    def add(self, point):
        self.score += point

    def get_score(self):
        return self.score

