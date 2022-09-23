from config import conf
import random
import pygame
import time

# ----Player----
from Player import Player
from Square import Square

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

        self.click_damage = 1
        self.square_list = []

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

            # Create groups
            self.enemies = pygame.sprite.Group()
            self.player = pygame.sprite.GroupSingle()

            sound.play("music", -1)

            # Returns false on game over
            while self.play():
                pass

            sound.stop("music")

    def play(self):
        """Returns false on game over, true on end of level"""

        self.getTicksLastFrame = 0
        self.background = lib.draw_background()
        self.spawn_player()

        self.playermoves = {"right": False, "left": False}
        tic = time.time()
        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise SystemExit
                elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                    key_down = event.type == pygame.KEYDOWN
                    if event.key == pygame.K_LEFT:
                        self.playermoves["left"] = key_down
                    elif event.key == pygame.K_RIGHT:
                        self.playermoves["right"] = key_down
                    elif key_down and event.key == pygame.K_ESCAPE:
                        self.player.sprite.kill()
                        pygame.event.clear()
                        return False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mousepos = pygame.mouse.get_pos()
                    # print("Clicked at",mousepos)
                    # TODO: click damage
                    for square in self.square_list:
                        if isInsideRectangle(mousepos, square.get_rect()):
                            square.point -= self.click_damage
                            if square.point <= 0:
                                self.square_list.remove(square)
                                print("Square destroyed")

            self.draw()

            for enemy in pygame.sprite.spritecollide(
                self.player.sprite, self.enemies, False
            ):
                if lib.detect_collision(self.player.sprite, enemy):
                    print("Overlap")
                    return False
            toc = time.time()
            if toc - tic > 10:  # 10s
                self.generate_square()
                tic = toc

    def generate_square(self):
        self.enemies.add(
            Square(
                size=[50, 50],
                pos=[
                    random.randint(0, WIDTH),
                    random.randint(0, HEIGHT_UPPER_BOUND_SQUARE),
                ],
                vector=[random.uniform(0, 1), random.uniform(0, 1)],
                speed=random.randint(1, 10),
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

        deltaTime = self.GetDeltaTime()
        # Player
        if self.player:
            self.player.update(deltaTime, self.playermoves)
            self.player.draw(self.screen)

        self.enemies.update()
        # for enemy in self.enemies:
        #     print(enemy.rect)
        self.enemies.draw(self.screen)

        pygame.display.update()
        self.clock.tick(FRAME_RATE)

    def GetDeltaTime(self):
        t = pygame.time.get_ticks()
        deltaTime = (t - self.getTicksLastFrame) / 1000.0
        self.getTicksLastFrame = t
        return deltaTime


if __name__ == "__main__":
    Game().begin()
