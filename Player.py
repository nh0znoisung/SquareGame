import pygame
from sound import sound

from locals import *
import lib

#### loading animation ####
def getWalk():
    base = pygame.image.load(lib.filename("PlayerAnimation/walk/Player (1).png"))
    re = [pygame.Surface(base.get_size(), pygame.SRCALPHA, 32) for _ in range(12)]
    re = [re[i].convert_alpha() for i in range(12)]
    [
        re[i].blit(
            pygame.image.load(
                lib.filename("PlayerAnimation/walk/Player (%d).png" % (i + 1))
            ),
            (-3, -13),
        )
        for i in range(12)
    ]
    return re


def getSlash():
    return [
        pygame.image.load(lib.filename("PlayerAnimation/slash/slash%d.png" % i))
        for i in range(7)
    ]


def getDash():
    return [
        pygame.image.load(lib.filename("PlayerAnimation/dash/dash%d.png" % i))
        for i in range(4)
    ]


def getSwordSlash():
    return [
        pygame.image.load(
            lib.filename("PlayerAnimation/saberslash/saberslash%d.png" % i)
        )
        for i in range(7)
    ]


def getDie():
    re = [
        pygame.image.load(lib.filename("PlayerAnimation/die/die0%d.png" % i))
        for i in range(10)
    ]
    return re[:2] + [re[2]] * 3 + re[2:]


###########################

#### animation utils ####
def scaleAnim(l):
    return [pygame.transform.scale2x(l[i]) for i in range(len(l))]


def flipAnim(l):
    return [pygame.transform.flip(l[i], True, False) for i in range(len(l))]


def initAnim(l, withFlipped: bool):
    return [l] + ([flipAnim(l)] if withFlipped else [l])


###########################


class Player(pygame.sprite.Sprite):
    class PlayerAnim:
        def __init__(self, player, walk, slash, dash, die, swordSlash):
            self.player = player
            self.idle = [[walk[0][0]], [walk[1][0]]]
            self.walk = walk
            self.slash = slash
            self.dash = dash
            self.die = die
            self.swordSlash = swordSlash

            self.curAnim = None
            self.animFlip = False
            self.swordSlashSprite = pygame.sprite.Sprite()
            self.swordSlashGroup = pygame.sprite.GroupSingle(self.swordSlashSprite)
            self.slashDone = True
            self.dashDone = 0
            self.dieDone = 0

        def goIdle(self):
            if self.curAnim is not self.idle:
                self.curAnim = self.idle
                self.animTime = 0
                self.animDuration = 1
                self.animSpriteOffset = 0

        def goWalk(self):
            if self.curAnim is not self.walk:
                self.curAnim = self.walk
                self.animSpriteOffset = 1
                self.animTime = 0
                self.animDuration = 1.0

        def goSlash(self):
            if self.curAnim is not self.slash:
                if not self.player.useStamina(50):
                    return
                self.curAnim = self.slash
                self.animSpriteOffset = 0
                self.animTime = 0
                self.animDuration = 0.4
                self.slashDone = False
                self.swordSlashSpritePos = pygame.mouse.get_pos()
                sound.play("slash")

        def goDash(self):
            if self.curAnim is not self.dash:
                self.curAnim = self.dash
                self.animSpriteOffset = 0
                self.animTime = 0
                self.animDuration = 0.2
                self.dashDone = 0
                sound.play("dash")

        def goDie(self):
            if self.curAnim is not self.die:
                self.curAnim = self.die
                self.animSpriteOffset = 0
                self.animTime = 0
                self.animDuration = 1
                self.dieDone = 0
                sound.play("die")

        def getSprite(self, delta=0) -> pygame.Surface:
            self.animTime += delta
            if self.animTime > self.animDuration:
                self.animTime -= self.animDuration
                if self.curAnim is self.walk:
                    self.animSpriteOffset = 2  # begin from sprite 2 if walk
                if self.curAnim is self.slash:
                    self.slashDone = True
                if self.curAnim is self.dash:
                    self.animSpriteOffset = 3
                    self.dashDone += 1
                if self.curAnim is self.die:
                    self.animSpriteOffset = 9
                    self.dieDone += 1

            # get sprite base on cur time and numsprite
            numSprite = len(self.curAnim[0]) - self.animSpriteOffset
            curIdx = (
                self.animSpriteOffset
                + int(self.animTime / self.animDuration * numSprite) % numSprite
            )

            if self.curAnim is self.slash:
                self.swordSlashSprite.image = self.swordSlash[self.animFlip][curIdx]
                self.swordSlashSprite.rect = self.swordSlashSprite.image.get_rect(
                    center=self.swordSlashSpritePos
                )

            return self.curAnim[self.animFlip][curIdx]

    def __init__(self, game, initialX, initialY, acceleration=1):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        #### init animations ####
        walkAnim = initAnim(scaleAnim(getWalk()), withFlipped=True)
        slashAnim = initAnim(scaleAnim(getSlash()), withFlipped=True)
        dashAnim = initAnim(scaleAnim(getDash()), withFlipped=True)
        dieAnim = initAnim(scaleAnim(getDie()), withFlipped=True)
        swordSlashAnim = initAnim(scaleAnim(getSwordSlash()), withFlipped=True)
        # init player anim object
        self.anim = Player.PlayerAnim(
            self, walkAnim, slashAnim, dashAnim, dieAnim, swordSlashAnim
        )
        self.anim.goIdle()
        ###########################

        self.image = self.anim.getSprite()
        self.rect = self.image.get_rect(topleft=(initialX, initialY))
        self.curX, self.curY = initialX, initialY
        self.v = 0
        self.acceleration = acceleration
        self.is_shield = False
        self.stamina = 100.0  # 100 %

    def useStamina(self, amount):
        amount = amount * STAMINA_MULTIPLIER[self.game.level]
        if self.stamina >= amount:
            self.stamina -= amount
            return True
        return False

    def recoverStamina(self, delta, recoverRate):
        self.stamina = min(100.0, self.stamina + delta * recoverRate)

    def activateShield(self):
        self.is_shield = True

    def deActivateShield(self):
        self.is_shield = False

    def draw_shield(self, screen):
        if self.is_shield:
            pygame.draw.circle(
                screen,
                "WHITE",
                (
                    self.curX + PLAYER_SIZE[0] / 2 - 7 + self.anim.animFlip * 10,
                    self.curY + PLAYER_SIZE[1] / 2,
                ),
                65,
                5,
            )

    def get_pos(self):
        return [self.curX, self.curY]

    def update(self, deltaTime, playermoves):
        self.v = 0

        if playermoves["die"]:
            self.anim.goDie()
        elif playermoves["slash"]:
            self.anim.goSlash()
            if self.anim.slashDone:
                playermoves["slash"] = False
                self.anim.goIdle()
        else:
            if playermoves["left"]:
                self.anim.animFlip = True
            if playermoves["right"]:
                self.anim.animFlip = False
            if playermoves["dash"]:
                self.v = self.acceleration * (1 - 2 * self.anim.animFlip) * 2
                self.anim.goDash()
                if not self.useStamina(250.0 * deltaTime) or self.anim.dashDone >= 2:
                    playermoves["dash"] = False
                    self.anim.goIdle()
            else:
                if playermoves["left"]:
                    self.v = -self.acceleration
                    self.anim.goWalk()
                elif playermoves["right"]:
                    self.v = self.acceleration
                    self.anim.goWalk()
                else:
                    self.anim.goIdle()

        self.curX += self.v * deltaTime
        self.curX = max(0, self.curX)
        self.curX = min(WIDTH - PLAYER_SIZE[0], self.curX)

        self.image = self.anim.getSprite(deltaTime)
        self.rect.topleft = (self.curX, self.curY)

        self.recoverStamina(deltaTime, BULLET1_COOLDOWN[self.game.level] * 100)
