import pygame
from locals import *


class Shields:
    def __init__(self):
        self.nums = SHIELD_MAX_NUMS
        self.shield = pygame.image.load("data/shield.png")
        self.shield = pygame.transform.scale(self.shield, SHIELD_SIZE)
    
    def display(self, screen, idx):
        screen.blit(self.shield, (WIDTH - int(idx) * (SHIELD_SIZE[0] + SHIELD_DELTA_SPACE) , BAR_HEIGHT))

    def draw(self, screen):
        for i in range(self.nums):
            self.display(screen, i + 1)
    
    def add(self):
        if self.get_nums()<SHIELD_MAX_NUMS:
            self.nums += 1
    def subtract(self):
        self.nums -= 1
    def get_nums(self):
        return self.nums