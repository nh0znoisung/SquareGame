from asyncore import write
from gc import get_objects
from tkinter import Button
from turtle import Screen
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

        self.is_pause = False
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

            # Create groups
            self.enemies = pygame.sprite.Group()
            self.player = pygame.sprite.GroupSingle()

            sound.play("music", -1)

            self.play()

            sound.stop("music")

    # def checkpause(e):
    #     for ev in e:
    #         if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
    #             if self.is_pause:
    #                 self.is_pause = False
    #             else:
    #                 quit(0)
    #         if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
    #             pause = not pause

    # running, pause = True, False
    # while running:
    #     events = pygame.event.get()
    #     checkquit(events)

    #     screen.fill((0,0,0))
    #     if pause:
    #         # draw pause screen
    #         screen.blit(text2,(10,200))
    #         screen.blit(text1,(230,100))

    #     else:
    #         # draw game
    #         # [...]

    #pygame.display.update() 


    def paused(self):
        sound.stop("music")
        paused = lib.render_text("Paused", 100) 
        self.screen.blit(paused, ((WIDTH/3),(HEIGHT/3)))

        while self.is_pause:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.is_pause = False
                    sound.play("music")
            #gameDisplay.fill(white)

            pygame.display.update()

    def play(self):
        """Returns false on game over, true on end of level"""
        self.getTicksLastFrame = 0

        self.click_damage = 1
        self.shields = Shields()
        self.is_shield = False
        self.score = Score()
        self.background = lib.draw_background()
        self.enemies.add(
            Square(size=[50, 50], pos=[50, 50], vector=[3.1, 1.3], speed=1)
        )
        self.enemies.add(Square(size=[50, 50], pos=[10, 100], vector=[1, 1.3], speed=1))

        self.spawn_player()

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
                        self.is_pause = True
                        self.paused()

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mousepos = pygame.mouse.get_pos()
                    # print("Clicked at",mousepos)
                    # TODO: click damage
                    for square in self.enemies:
                        if isInsideRectangle(mousepos, square.get_rect()):
                            square.point -= self.click_damage
                            if square.point <= 0:
                                self.score.add(square.origpoint)
                                square.kill()
                                print("Square destroyed")

            self.draw()

            # player & enemy collision
            for enemy in pygame.sprite.spritecollide(
                self.player.sprite, self.enemies, False
            ):
                if lib.detect_collision(self.player.sprite, enemy):
                    if not self.is_shield:

                        if conf.is_highscore(self.score.get_score()):
                            sound.play("explode", 0)
                            sound.stop("music")
                            font = pygame.font.Font(None, 32)
                            clock = pygame.time.Clock()
                            input_box = pygame.Rect(WRITENAME_WIDTH+70, WRITENAME_HEIGHT+70, 380, 32)
                            color_inactive = pygame.Color('lightskyblue3')
                            color_active = pygame.Color('dodgerblue2')
                            color = color_inactive
                            active = False
                            text = ''
                            done = False

                            while not done:
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        raise SystemExit
                                    if event.type == pygame.MOUSEBUTTONDOWN:
                                        # If the user clicked on the input_box rect.
                                        if input_box.collidepoint(event.pos):
                                            # Toggle the active variable.
                                            active = not active
                                        else:
                                            active = False
                                        # Change the current color of the input box.
                                        color = color_active if active else color_inactive
                                    if event.type == pygame.KEYDOWN:
                                        if active:
                                            if event.key == pygame.K_RETURN:
                                                done = True
                                            elif event.key == pygame.K_BACKSPACE:
                                                text = text[:-1]
                                            else:
                                                text += event.unicode
                                background_image = pygame.image.load("data/gameover.png")
                                background_image = pygame.transform.scale(background_image, [WIDTH, HEIGHT])

                                
                                
                                self.screen.fill((30, 30, 30))
                                # Render the current text.
                                txt_surface = font.render(text, True, color)
                                # Resize the box if the text is too long.
                                width = max(200, txt_surface.get_width()+10)
                                #input_box.w = width
                                # Blit the text.
                                self.screen.blit(background_image, [0, 0])
                                writename = lib.render_text("Write your name", 60, (0x00, 0x99, 0xFF)) 
                                self.screen.blit(writename, (WRITENAME_WIDTH,WRITENAME_HEIGHT))
                                self.screen.blit(txt_surface, (WRITENAME_WIDTH+73, WRITENAME_HEIGHT+73))
                                # Blit the input_box rect.
                                pygame.draw.rect(self.screen, color, input_box, 2)

                                pygame.display.flip()
                                clock.tick(30)
                                
                            conf.register_highscore(text, self.score.get_score())
                            
                            return False
                        else:
                            sound.play("explode", 0)
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

        self.enemies.update()
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
        self.clock.tick(FRAME_RATE)

    def GetDeltaTime(self):
        t = pygame.time.get_ticks()
        deltaTime = (t - self.getTicksLastFrame) / 1000.0
        self.getTicksLastFrame = t
        return deltaTime


if __name__ == "__main__":
    Game().begin()
