from config import conf
import random
import pygame
from pygame.locals import *
import time
from Shields import Shields
from Score import Score

# ----Player----
from Player import Player
from Square import Square
from Bullet import Bullet

pygame.init()

import lib

from menu import Menu
from sound import sound

from locals import *


class Game:
    square_list: list

    def __init__(self):

        self.set_screen()
        pygame.display.set_caption(GAME)

        self.clock = pygame.time.Clock()

    def set_screen(self):
        """Sets (resets) the self.screen variable with the proper fullscreen"""
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

            sound.play("music", -1)

            self.play()

            sound.stop("music")

    def play(self):
        """Returns false on game over, true on end of level"""
        self.enemies = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        self.click_damage = 1
        self.shields = Shields()
        self.is_shield = False
        self.score = Score()
        self.background = lib.draw_background()
        self.spawn_player()
        self.generate_square()

        self.playermoves = {"right": False, "left": False}

        tic_generate_square = time.time()
        tic_shield = time.time()
        tic_shield_cooldown = time.time()
        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise SystemExit
                elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                    key_down = event.type == pygame.KEYDOWN
                    if event.key == pygame.K_a:
                        self.playermoves["left"] = key_down
                    elif event.key == pygame.K_d:
                        self.playermoves["right"] = key_down
                    elif key_down and event.key == pygame.K_SPACE:
                        if not self.is_shield and self.shields.get_nums() > 0:
                            self.is_shield = True
                            self.shields.subtract()
                            tic_shield = time.time()
                    elif key_down and event.key == pygame.K_ESCAPE:
                        pygame.event.clear()
                        return False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mousepos = pygame.mouse.get_pos()
                    # print("Clicked at",mousepos)
                    # TODO: click damage
                    for square in self.enemies:
                        if isInsideRectangle(mousepos, square.get_rect()):
                            square.point -= self.click_damage
                            sound.play("hit")
                            if square.point <= 0:
                                self.score.add(square.origpoint)
                                sound.play("explode")
                                square.kill()
                                print("Square destroyed")

            self.draw()

            # player & enemy collision
            for enemy in pygame.sprite.spritecollide(
                self.player.sprite, self.enemies, False
            ):
                if lib.detect_collision(self.player.sprite, enemy):
                    if not self.is_shield:
                        sound.play("die", 0)
                        return False

            # check shield still active
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

            toc_generate_square = time.time()
            if toc_generate_square - tic_generate_square > 10:  # 10s
                self.generate_square()
                tic_generate_square = toc_generate_square

    def generate_square(self):
        self.enemies.add(
            Square(
                size=[50, 50],
                pos=[
                    random.randint(0, WIDTH),
                    random.randint(0, HEIGHT_UPPER_BOUND_SQUARE),
                ],
                vector=[random.uniform(0, 1), random.uniform(0, 1)],
                speed=random.randint(50, 300),
            )
        )

    def spawn_player(self):
        self.player.add(Player(100, 450, 300))

    def reset_game(self):
        # TODO
        # reset game
        pass

    def draw(self):
        """Draw and update the game"""
        self.screen.blit(self.background, (0, 0))

        deltaTime = self.clock.tick(FRAME_RATE) / 1000.0

        # Player
        self.enemies.update(deltaTime)
        self.enemies.draw(self.screen)

        if self.player:
            self.player.update(deltaTime, self.playermoves)
            self.player.draw(self.screen)

        # Shield
        self.player.sprite.draw_shield(self.screen, self.is_shield)
        # print(self.is_shield)

        # Score
        self.score.update(self.screen)

        self.shields.draw(self.screen)

        pygame.display.update()


if __name__ == "__main__":
    Game().begin()
