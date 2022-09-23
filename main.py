
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
		
		sprites.game = self
		self.square_list = []

		self.shields = Shields()
		self.is_shield = False
		self.score = Score()
		self.bullet_list = []
		self.bullet_mode = 1
		self.level = 0
		self.tic_bullet_1 = -1

		# Setup challenge
		self.generate_square()
		self.generate_square()


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
			# print(conf.sound)
			
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
		tic_shield_cooldown = -1
		

		while True:
			if self.score.get_score() >= LEVEL_SCORE_UPPER_BOUND[self.level]:
				self.level += 1
				print("Current level: ", self.level)
			for event in pygame.event.get():
				# print(pygame.mouse.get_pos())
				if event.type == pygame.QUIT:
					raise SystemExit
				elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
					key_down = (event.type == pygame.KEYDOWN)
					if event.key == pygame.K_LEFT or event.key == pygame.K_a:
						self.playermoves['left'] = key_down
					elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
						self.playermoves['right'] = key_down
					elif key_down and event.key == pygame.K_w:
						self.bullet_mode = 1 - self.bullet_mode
					elif key_down and event.key == pygame.K_SPACE:
						if not self.is_shield and self.shields.get_nums() > 0:
							if self.shields.get_nums() == SHIELD_MAX_NUMS:
								tic_shield_cooldown = time.time()
							self.is_shield = True
							self.shields.subtract()
							tic_shield = time.time()
					elif key_down and event.key == pygame.K_ESCAPE:
						self.player.kill()
						pygame.event.clear()
						return False
				elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
					mousepos = pygame.mouse.get_pos()
					toc_bullet_1 = time.time()
					if toc_bullet_1 - self.tic_bullet_1 >= BULLET1_COOLDOWN[self.level]:
						self.shoot(mousepos, self.Player.get_pos())
						if self.bullet_mode == 0:
							self.tic_bullet_1 = toc_bullet_1

								
			if self.is_shield:
				toc_shield = time.time()
				if toc_shield - tic_shield > SHIELD_PROTECT:
					tic_shield = toc_shield 
					self.is_shield = False
					

			if tic_shield_cooldown != -1:
				toc_shield_cooldown = time.time()
				if toc_shield_cooldown - tic_shield_cooldown > SHIELD_COOLDOWN:
					self.shields.add()
					if self.shields.get_nums() == SHIELD_MAX_NUMS:
						tic_shield_cooldown = -1
					else:
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
				if ok and self.bullet_mode == 1:
					self.bullet_list.remove(bullet)
						
			# Remove bullet that is out of screen
			for bullet in self.bullet_list:
				pos_x, pos_y = bullet.get_pos()
				if pos_x < 0 or pos_x > WIDTH or pos_y < 0 or pos_y > HEIGHT:
					self.bullet_list.remove(bullet)

			self.draw()				
			
			for square in self.square_list:
				if(isRectangleOverlap(square.get_rect(), self.Player.get_rect())):
					if not self.is_shield:
						return False
			
			# TODO: generate level
			toc_generate_square = time.time()
			if (toc_generate_square - tic_generate_square > PERIOD_GENRATE[self.level]): #10s
				for i in range(random.randint(1,GENERATE_SQUARE[self.level])):
					self.generate_square()
				tic_generate_square = toc_generate_square


	def draw_cooldown(self):
		pygame.draw.arc(self.screen, "BLUE", 
		(self.Player.curX + 5, self.Player.curY + 19.5, COOLDOWN_RADIUS, COOLDOWN_RADIUS),
		0, (min(time.time() - self.tic_bullet_1, BULLET1_COOLDOWN[self.level])) * math.pi*2 / BULLET1_COOLDOWN[self.level], 
		4)

	def shoot(self, mousepos, player_pos):
		vector = [mousepos[0] - player_pos[0], mousepos[1] - player_pos[1]]
		if self.bullet_mode == 0:
			self.shoot_bullet_1(player_pos, vector)
		elif self.bullet_mode == 1:
			self.shoot_bullet_2(player_pos, vector)
			
	def shoot_bullet_1(self, player_pos, vector):
		self.bullet_list.append(Bullet(player_pos, vector, self.bullet_mode, BULLET1_SPEED[self.level], BULLET1_DAMAGE[self.level]))
	
	def shoot_bullet_2(self, player_pos, vector):
		for i in range(BULLET2_SHOOT_NUMS[self.level]//2 + 1):
			if i == 0:
				self.shoot_bullet_2_util(player_pos, vector, 0)
			else:
				self.shoot_bullet_2_util(player_pos, vector, BULLET2_SHOOT_ANGLE[self.level]*i)
				self.shoot_bullet_2_util(player_pos, vector, -BULLET2_SHOOT_ANGLE[self.level]*i)


	def shoot_bullet_2_util(self, player_pos, vector, angel):
		new_vector = rotateVector(vector, angel)
		self.bullet_list.append(Bullet(player_pos, new_vector, self.bullet_mode, BULLET2_SPEED[self.level], BULLET2_DAMAGE[self.level]))
		
	
	# setup level
	def generate_square(self):
		# TODO
		self.square_list.append(Square(size = [random.choice(SQUARE_SIZE)]*2, 
			pos = [random.randint(0, WIDTH),random.randint(0, HEIGHT_UPPER_BOUND_SQUARE[self.level])], 
			vector=[random.uniform(0, 1),random.uniform(0, 1)], 
			speed=random.randint(SPEED_LOWER_BOUND_SQUARE[self.level], SPEED_UPPER_BOUND_SQUARE[self.level]),
			idx = random.randint(INDEX_LOWER_BOUND_SQUARE[self.level], INDEX_UPPER_BOUND_SQUARE[self.level])))


	def draw(self):
		'''Draw and update the game'''
		
		self.screen.blit(self.background, (0, 0))
  		#Player
		if not self.hasSpawnPlayer:
			self.Player = Player(self.screen, WIDTH/2-50, 450, 300)
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

		#Cooldown
		self.draw_cooldown()

		pygame.display.update()
		self.clock.tick(FRAME_RATE)
	

	def GetDeltaTime(self):
		t = pygame.time.get_ticks()
		deltaTime = (t - self.getTicksLastFrame) / 1000.0
		self.getTicksLastFrame = t
		return deltaTime
 

if __name__ == '__main__':    
	Game().begin()
