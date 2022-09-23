import pygame

from locals import *


class Player(pygame.sprite.Sprite):
    def __init__(self, intialX, intialY, acceleration=1):
        pygame.sprite.Sprite.__init__(self)
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
            pygame.image.load("data/PlayerAnimation/Player (12).png"),
        ]
        for i in range(len(self.player)):
            self.player[i] = pygame.transform.scale(self.player[i], PLAYER_SIZE)
        self.playerFlipped = [
            pygame.transform.flip(sprite, True, False) for sprite in self.player
        ]
        self.curX = intialX
        self.curY = intialY
        self.acceleration = acceleration
        self.curIndexAnimation = 0
        self.numAnimation = 12
        self.animTime = 0
        self.animDuration = 1
        self.animSpriteOffset = 1
        self.animFlip = False

        self.image = self.player[self.curIndexAnimation]
        self.rect = self.image.get_rect()

    def draw_shield(self, screen, is_shield):
        if is_shield:
            pygame.draw.circle(
                screen,
                "YELLOW",
                (
                    self.curX + PLAYER_SIZE[0] / 2 - 5,
                    self.curY + PLAYER_SIZE[1] / 2 + 9.5,
                ),
                50,
                5,
            )

    def update(self, deltaTime, playermoves):
        self.rect.topleft = [self.curX, self.curY]
        self.animTime += deltaTime

        if playermoves["left"]:
            self.animFlip = True
            if self.curX > self.acceleration * deltaTime:
                self.curX -= self.acceleration * deltaTime
            else:
                self.curX = 0
            self.UpdateAnimation()

        elif playermoves["right"]:
            self.animFlip = False
            if self.curX < WIDTH - PLAYER_SIZE[0] - self.acceleration * deltaTime:
                self.curX += self.acceleration * deltaTime
            else:
                self.curX = WIDTH - PLAYER_SIZE[0]
            self.UpdateAnimation()
        else:
            self.curIndexAnimation = 0
            self.animTime = 0
            self.animSpriteOffset = 1

        self.image = (
            self.player[self.curIndexAnimation]
            if not self.animFlip
            else self.playerFlipped[self.curIndexAnimation]
        )

    def UpdateAnimation(self):
        if self.animTime > self.animDuration:
            self.animTime - self.animDuration
            self.animSpriteOffset = 2  # begin from sprite 2
        self.curIndexAnimation = self.animSpriteOffset + int(
            self.animTime
            / self.animDuration
            * (self.numAnimation - self.animSpriteOffset)
        ) % (self.numAnimation - self.animSpriteOffset)
