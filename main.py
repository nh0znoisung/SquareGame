
from config import conf
import random
import pygame

pygame.init()

import lib
import sprites

from menu import Menu
from sound import sound

from locals import *

class Game:

	def __init__(self):
		
		self.set_screen()
		pygame.display.set_caption(GAME)
		
		self.clock = pygame.time.Clock()
		
		
		sprites.game = self
		
	
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
			
			# Display the menu
			menu.show()
			
			
			# Create groups
			self.sprites = sprites.SpriteGroup()
			self.enemies = sprites.SpriteGroup()
			self.player = sprites.PlayerGroup()
			
			sound.play("music", -1)
			print(conf.sound)
			
			# Returns false on game over
			while self.play():
				pass
			
			sound.stop("music")
	 
			
	def play(self):
		''' Returns false on game over, true on end of level'''

		self.background = lib.draw_background()
		self.spawn_player()
		
		self.playermoves = {
			'right':False,
			'left': False
		}
		
		while True:
			
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					raise SystemExit
				elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
					key_down = (event.type == pygame.KEYDOWN)
					if event.key == pygame.K_LEFT:
						self.playermoves['left'] = key_down
					elif event.key == pygame.K_RIGHT:
						self.playermoves['right'] = key_down
					elif key_down and event.key == pygame.K_ESCAPE:
						self.player.kill()
						pygame.event.clear()
						return False
				elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
					mousepos = pygame.mouse.get_pos()
					print("Clicked at",mousepos)
					# TODO
					pass
			
			self.draw()
			player = self.player.sprite
					
			if player:
				if self.playermoves['left']:
					self.player.left()
				if self.playermoves['right']:
					self.player.right()
			
			# Player -> enemy collisions
			if player :
				for enemy in pygame.sprite.spritecollide(player, self.enemies, False):
					if lib.detect_collision(player, enemy):
						#lose here
						pass
					
			num_enemies = len(self.enemies)
		
			if num_enemies == 0:
				x_pos = random.randint(0, WIDTH - 1)
				y_pos = random.randint(0, HEIGHT - 1)
				sprites.Enemy((x_pos,y_pos))


	def draw(self):
		'''Draw and update the game'''
		
		self.screen.blit(self.background, (0, 0))
		
		self.sprites.update()
		self.sprites.draw(self.screen)
		
		pygame.display.update()
		self.clock.tick(FRAME_RATE)


	def spawn_player(self):
		sprites.Player((WIDTH/2, HEIGHT/2))
	

if __name__ == '__main__':    
	Game().begin()
