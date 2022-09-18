import math
import pygame

import lib
from locals import *

# Needs to be set to a Game object before we can use these sprites
game = None


class SpriteGroup(pygame.sprite.Group):
    '''A container for sprites.'''
    pass


class PlayerGroup(pygame.sprite.GroupSingle):
    '''A container for the player'''

    def __getattr__(self, attr):
        '''If a player exists, get that attribute, otherwise do nothing.'''
        
        if self:
            return getattr(self.sprite, attr)
        else:
            return lib.none_func

class Sprite(pygame.sprite.Sprite):
    '''Abstract sprite class.'''
    
    def __init__(self, location, size, r, vel):
        '''Create an abstract ceneterd sprite at location (x, y) with
        size (l, w), direction r, and speed vel (negative for reverse).
        You can give these values 0 if they're unneed except for size.'''
        
        x, y = location
        
        pygame.sprite.Sprite.__init__(self)
        
        self.x, self.y, self.r, self.vel = float(x), float(y), float(r), float(vel)
        
        self.image = pygame.Surface(size)

        self.image.set_colorkey(TRANSPARENT)
        
        self.image.fill(TRANSPARENT)
            
        self.rect = self.image.get_rect(center=location)
        
        game.sprites.add(self)
        
    def update(self):
        '''Move the sprite according to the vel and r properties'''
        
        if self.vel:
        
            self.x = (self.x - self.vel * math.sin(self.r)) % WIDTH
            self.y = (self.y - self.vel * math.cos(self.r)) % HEIGHT
            
            self.rect.center = (self.x, self.y)

class Player(Sprite):
    SIZE = (100,100)

    def __init__(self, location):
        Sprite.__init__(self,location,self.SIZE,0,0)
        game.player.add(self)
        pass
    
    def update(self):
        Sprite.update(self)
        pass
            
    def right(self):   
        pass
        
    def left(self):  
        pass

    def kill(self):
        Sprite.kill(self)
        pass

class Enemy(Sprite):
    SIZE = (100,100)

    def __init__(self, location):
        Sprite.__init__(self,location,self.SIZE,0,0)
        game.enemies.add(self)
        pass

    def clicked(self):
        pass

    def update(self):
        Sprite.update(self)
        pass
        
    def kill(self):
        Sprite.kill(self)
        pass