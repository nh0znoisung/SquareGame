from pickle import TRUE
from turtle import right
import pygame

from locals import *

class Player:
    def __init__(self, scene, intialX, intialY, acceleration = 1):
        self.player = [
                        pygame.image.load("data/PlayerAnimation/Player (1).png"),
                        pygame.image.load("data/PlayerAnimation/Player (2).png"),
                        pygame.image.load("data/PlayerAnimation/Player (3).png"),
                        pygame.image.load("data/PlayerAnimation/Player (4).png"),
                        pygame.image.load("data/PlayerAnimation/Player (5).png"),
                        pygame.image.load("data/PlayerAnimation/Player (6).png"),
                        pygame.image.load("data/PlayerAnimation/Player (7).png"),
                        pygame.image.load("data/PlayerAnimation/Player (8).png"),
                        pygame.image.load("data/PlayerAnimation/Player (9).png"),
                        pygame.image.load("data/PlayerAnimation/Player (10).png"),
                        pygame.image.load("data/PlayerAnimation/Player (11).png"),
                        pygame.image.load("data/PlayerAnimation/Player (12).png")
                       ]
        self.curX = intialX
        self.curY = intialY
        self.acceleration = acceleration
        self.curIndexAnimation = 0
        self.numAnimation = 12
        scene.blit(self.player[self.curIndexAnimation], (intialX, intialY)) 

    def get_rect(self):
        return [self.curX, self.curY, self.curX + PLAYER_SIZE[0], self.curY + PLAYER_SIZE[1]]

    def Update(self, dealtaTime, scene, playermoves):
        flip = False
        
        if playermoves['left']:
            if self.curX > self.acceleration * dealtaTime:
                self.curX -= self.acceleration * dealtaTime
            else:
                self.curX = 0
            self.UpdateAnimation()
            flip = True
            
        elif playermoves['right']:
            if self.curX < WIDTH - PLAYER_SIZE[0] - self.acceleration * dealtaTime:
                self.curX += self.acceleration * dealtaTime
            else:
                self.curX = WIDTH - PLAYER_SIZE[0]
            self.UpdateAnimation()
        else:
            self.curIndexAnimation = 0 
  
        scene.blit(pygame.transform.scale(pygame.transform.flip(self.player[self.curIndexAnimation], flip, False), PLAYER_SIZE), 
                   
                   (self.curX, self.curY))
    
    def UpdateAnimation(self):
        self.curIndexAnimation += 1
        if self.curIndexAnimation == self.numAnimation:
            self.curIndexAnimation = 1    
    