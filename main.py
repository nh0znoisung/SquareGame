
from re import S
from config import conf
import random
import pygame
from pygame.locals import *
import time
from Shields import Shields
from Score import Score

#----Player----
from Player import Player
from Square import Square
from Bullet import Bullet

pygame.init()

import lib
import sprites

from menu import Menu
from sound import sound

from locals import *

class Game:
	square_list: list

	def __init__(self):
		
		self.set_screen()
		pygame.display.set_caption(GAME)
		
		self.clock = pygame.time.Clock()
		
		self.click_damage = 1
		sprites.game = self
		self.square_list = []
		# self.square_list.append(Square(size = [100,100], pos = [200,200]))
		self.square_list.append(Square(size = [50,50], pos = [50,50], vector=[3.1,1.3], speed=1))
		self.square_list.append(Square(size = [50,50], pos = [10,100], vector=[1,1.3], speed=1))
		self.shields = Shields()
		self.is_shield = False
		self.score = Score()
		self.bullet_list = []
		self.bullet_mode = 1
	
	def set_screen(self):
		'''Sets (resets) the self.screen variable with the proper fullscreen'''
		if conf.fullscreen:
			fullscreen = pygame.FULLSCREEN
		else:
			fullscreen = 0
		self.screen = pygame.display.set_mode((WIDTH, HEIGHT), fullscreen)

		
	def begin(self):
		
		menu = Menu(self)
		
		while True:
			self.__init__()
			# Display the menu
			menu.show()
			
			
			# Create groups
			self.sprites = sprites.SpriteGroup()
			self.enemies = sprites.SpriteGroup()
			#self.player = sprites.PlayerGroup()
			
			sound.play("music", -1)
			print(conf.sound)
			
			# Returns false on game over
			while self.play():
				pass
				
			
			sound.stop("music")
	 
			
	def play(self):
		''' Returns false on game over, true on end of level'''

		self.background = lib.draw_background()
		self.hasSpawnPlayer = False
		
		self.playermoves = {
			'right':False,
			'left': False
		}
		tic_generate_square = time.time()
		tic_shield = time.time()
		tic_shield_cooldown = time.time()
		while True:
			
			for event in pygame.event.get():
				# print(pygame.mouse.get_pos())
				if event.type == pygame.QUIT:
					raise SystemExit
					# 
				elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
					key_down = (event.type == pygame.KEYDOWN)
					if event.key == pygame.K_LEFT or event.key == pygame.K_a:
						self.playermoves['left'] = key_down
					elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
						self.playermoves['right'] = key_down
					elif key_down and event.key == pygame.K_s:
						self.bullet_mode = 1 - self.bullet_mode
						print(self.bullet_mode)
					elif key_down and event.key == pygame.K_SPACE:
						if not self.is_shield and self.shields.get_nums() > 0:
							self.is_shield = True
							self.shields.subtract()
							tic_shield = time.time()
					elif key_down and event.key == pygame.K_ESCAPE:
						self.player.kill()
						pygame.event.clear()
						return False
				elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
					# TODO: click damage
					mousepos = pygame.mouse.get_pos()
					self.shoot(mousepos, self.Player.get_pos())
								
			if self.is_shield:
				toc_shield = time.time()
				if toc_shield - tic_shield > SHIELD_PROTECT:
					tic_shield = toc_shield 
					self.is_shield = False
					

			if self.shields.get_nums() < SHIELD_MAX_NUMS:
				toc_shield_cooldown = time.time()
				if toc_shield_cooldown - tic_shield_cooldown > SHIELD_COOLDOWN:
					self.shields.add()
					tic_shield_cooldown = toc_shield_cooldown
			
			# Collision bullet and square
			for bullet in self.bullet_list:
				ok = False
				for square in self.square_list:
					if isInsideRectangle(bullet.get_pos(), square.get_rect()):
						ok = True
						square.point -= bullet.damage
						if square.point <= 0:
							self.score.add(square.get_point())
							self.square_list.remove(square)	
				if ok:
					self.bullet_list.remove(bullet)
						
			self.draw()				
			
			for square in self.square_list:
				if(isRectangleOverlap(square.get_rect(), self.Player.get_rect())):
					if not self.is_shield:
						return False
			
			# TODO: generate level
			toc_generate_square = time.time()
			if (toc_generate_square - tic_generate_square > 10): #10s
				self.generate_square()
				tic_generate_square = toc_generate_square



	def shoot(self, mousepos, player_pos):
		vector = [mousepos[0] - player_pos[0], mousepos[1] - player_pos[1]]
		if self.bullet_mode == 0:
			self.bullet_list.append(Bullet(player_pos, vector, self.bullet_mode))
		elif self.bullet_mode == 1:
			self.bullet_add(player_pos, vector, 0)
			self.bullet_add(player_pos, vector, 30)
			self.bullet_add(player_pos, vector, -30)
	def bullet_add(self, player_pos, vector, angel):
		new_vector  = rotateVector(vector, angel)
		self.bullet_list.append(Bullet(player_pos, new_vector, self.bullet_mode))
		

	def set_level(self): pass

	def generate_square(self):
		# TODO
		# setup level
		self.square_list.append(Square(size = [50,50], pos = [random.randint(0, WIDTH),random.randint(0, HEIGHT_UPPER_BOUND_SQUARE)], vector=[random.uniform(0, 1),random.uniform(0, 1)], speed=random.randint(1,10)))


	def draw(self):
		'''Draw and update the game'''
		
		self.screen.blit(self.background, (0, 0))
		
  		#Player
		if not self.hasSpawnPlayer:
			self.Player = Player(self.screen, 100, 450, 300)
			self.hasSpawnPlayer = True
			self.getTicksLastFrame = 0
		else:
			self.Player.Update(self.GetDeltaTime(), self.screen, self.playermoves)

		
  		#self.sprites.update()
		self.sprites.draw(self.screen)

		#Shield Player
		self.Player.draw_shield(self.screen, self.is_shield)

		#Score
		self.score.update(self.screen)

		#Bullet
		for bullet in self.bullet_list:
			bullet.update(self.screen)

		#Square
		for square in self.square_list:
			square.update(self.screen)

		#Shield
		self.shields.draw(self.screen)

		pygame.display.update()
		self.clock.tick(FRAME_RATE)
	

	def GetDeltaTime(self):
		t = pygame.time.get_ticks()
		deltaTime = (t - self.getTicksLastFrame) / 1000.0
		self.getTicksLastFrame = t
		return deltaTime
 

if __name__ == '__main__':    
	Game().begin()
