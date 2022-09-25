from config import conf
import random
import pygame
from pygame.locals import *
from collections import defaultdict

pygame.mixer.pre_init(44100, -16, 2, 1024 * 3)
pygame.init()

from Shields import Shields
from Score import Score
from Timer import Timer
from HitCount import HitCount

# ----Player----
from Player import Player
from Square import Square
from Bullet import Bullet

import lib

from menu import Menu
from sound import sound

from locals import *


class Game:
    class Scheduler:
        def __init__(self):
            self.jobMap = defaultdict(list)  # k=time, v=job

        def addJob(self, waitSeconds, *jobs):
            t = pygame.time.get_ticks()
            self.jobMap[t + int(waitSeconds * 1000)] += jobs

        def proccess(self):
            t = pygame.time.get_ticks()
            jM = self.jobMap
            self.jobMap = defaultdict(list)
            for k, v in jM.items():
                if k < t:
                    [fun() for fun in v]
                else:
                    self.jobMap[k] += v
            del jM

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

    def paused(self):
        sound.stop("music")
        pausedFont = pygame.font.SysFont("CopperPlate Gothic", 100, bold=True)
        pausedText = pausedFont.render("PAUSED", True, "WHITE")
        pausedTextSize = pausedFont.size("PAUSED")
        self.screen.blit(
            pausedText,
            (
                int(WIDTH / 2 - pausedTextSize[0] / 2),
                int(HEIGHT / 2 - pausedTextSize[1] / 2),
            ),
        )

        while self.is_pause:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.is_pause = False
                    sound.play("music")
            # gameDisplay.fill(white)
            self.clock.tick(FRAME_RATE)
            pygame.display.update()

    def play(self):
        """Returns false on game over, true on end of level"""
        self.enemiesGroup = pygame.sprite.Group()
        self.playerGroup = pygame.sprite.GroupSingle()
        self.isGameOver = False
        self.scheduler = Game.Scheduler()
        self.nextSquareTime = 5
        self.level = 0
        print("Current level: ", self.level)

        self.bullet_list = []
        self.bullet_mode = 1
        self.click_damage = 200
        self.shields = Shields()
        self.score = Score()
        self.timer = Timer()
        self.hit_count = HitCount()
        self.slash_hit = False
        self.background = lib.draw_background_main()
        self.spawn_player()
        self.generate_square()

        self.playermoves = {
            "right": False,
            "left": False,
            "slash": False,
            "dash": False,
            "die": False,
            "shoot": False,
        }

        while True:
            if self.score.get_score() >= LEVEL_SCORE_UPPER_BOUND[self.level]:
                self.level += 1
                print("Current level: ", self.level)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise SystemExit
                elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                    key_down = event.type == pygame.KEYDOWN
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        self.playermoves["left"] = key_down
                    elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        self.playermoves["right"] = key_down
                    elif event.key == pygame.K_LSHIFT:
                        self.playermoves["dash"] = key_down
                    elif key_down and event.key == pygame.K_w:
                        self.bullet_mode = 1 - self.bullet_mode
                    elif key_down and event.key == pygame.K_SPACE:
                        if not self.player.is_shield and self.shields.get_nums() > 0:
                            self.shields.subtract()
                            self.player.activateShield()
                            self.scheduler.addJob(SHIELD_COOLDOWN, self.shields.add)
                            self.scheduler.addJob(
                                SHIELD_PROTECT, self.player.deActivateShield
                            )
                            sound.play("shield")
                    elif key_down and event.key == pygame.K_ESCAPE:
                        self.is_pause = True
                        self.paused()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.isGameOver:
                        pass
                    elif event.button == 1:  # left-click
                        self.playermoves["shoot"] = True
                    elif event.button == 3:  # right-click
                        self.playermoves["slash"] = True
                        self.hit_count.add_total(1)
                        self.slash_hit = False
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.playermoves["shoot"] = False

            # Collision bullet and square
            for bullet in self.bullet_list:
                ok = False
                for square in self.enemiesGroup:
                    if isInsideRectangle(bullet.get_pos(), square.get_rect()):
                        ok = True
                        square.point -= bullet.damage
                        if square.point <= 0:
                            self.score.add(square.get_point())
                            square.kill()
                if ok and not bullet.is_hit:
                    self.hit_count.add_hit(1)
                    bullet.is_hit = True

                if ok and bullet.mode == 1:
                    self.bullet_list.remove(bullet)

            # Remove bullet that is out of screen
            for bullet in self.bullet_list:
                pos_x, pos_y = bullet.get_pos()
                if pos_x < 0 or pos_x > WIDTH or pos_y < 0 or pos_y > HEIGHT:
                    self.bullet_list.remove(bullet)

            deltaTime = self.clock.tick(FRAME_RATE) / 1000.0
            self.draw(deltaTime)

            # player & enemy collision
            if not self.isGameOver:
                for enemy in pygame.sprite.spritecollide(
                    self.player, self.enemiesGroup, False
                ):
                    if lib.detect_collision(self.player, enemy):
                        if not self.player.is_shield:
                            self.playermoves["die"] = True
                            self.isGameOver = True

            # swordslash & enemy collision
            if not self.player.anim.slashDone:
                for enemy in pygame.sprite.spritecollide(
                    self.player.anim.swordSlashSprite, self.enemiesGroup, False
                ):
                    if lib.detect_collision(self.player.anim.swordSlashSprite, enemy):
                        if not self.slash_hit:
                            self.hit_count.add_hit(1)
                            self.slash_hit = True
                        enemy.point -= (
                            self.click_damage * deltaTime * SLASH_DAMAGE[self.level]
                        )
                        if enemy.point <= 0:
                            self.score.add(enemy.get_point())
                            enemy.kill()

            self.scheduler.proccess()

            if self.isGameOver and self.player.anim.dieDone >= 2:
                self.gameOver()
                return False
            self.timer.add_timer(deltaTime)

    def gameOver(self):
        if conf.is_highscore(self.score.get_score()):
            sound.play("explode", 0)
            sound.stop("music")
            font = pygame.font.Font(None, 32)
            clock = pygame.time.Clock()
            input_box = pygame.Rect(
                WIDTH / 2 - INPUT_WIDTH / 2,
                500 - INPUT_HEIGHT / 2,
                INPUT_WIDTH,
                INPUT_HEIGHT,
            )
            color_inactive = pygame.Color("lightskyblue3")
            color_active = pygame.Color("dodgerblue2")
            active = True  # Default on selected
            color = color_active
            text = ""
            done = False

            while not done:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        raise SystemExit
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # If the user clicked on the input_box rect.
                        if input_box.collidepoint(event.pos):
                            # Toggle the active variable.
                            active = True
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
                            elif event.key != pygame.K_SPACE:
                                text += event.unicode
                background_image = pygame.image.load("data/gameover.png")
                background_size = [400, 400]
                background_image = pygame.transform.scale(
                    background_image, background_size
                )

                self.screen.fill((30, 30, 30))

                # Blit the background
                self.screen.blit(
                    background_image,
                    [
                        WIDTH / 2 - background_size[0] / 2,
                        200 - background_size[1] / 2,
                    ],
                )

                # Blit the writename
                writenameFont = pygame.font.SysFont("CopperPlate Gothic", 60, bold=True)
                writenameText = writenameFont.render(
                    "WRITE YOUR NAME", True, (0x00, 0x99, 0xFF)
                )
                writenameTextSize = writenameFont.size("WRITE YOUR NAME")
                self.screen.blit(
                    writenameText,
                    (
                        WIDTH / 2 - writenameTextSize[0] / 2,
                        425 - writenameTextSize[1] / 2,
                    ),
                )

                # Blit the input_box rect
                pygame.draw.rect(self.screen, color, input_box, 2)

                # Blit the current text.
                txt_surface = font.render(text, True, color)
                self.screen.blit(txt_surface, (input_box[0] + 5, input_box[1] + 5))

                pygame.display.flip()
                clock.tick(30)

            conf.register_highscore(text, self.score.get_score())

    def draw_cooldown(self):
        pygame.draw.arc(
            self.screen,
            "ORANGE" if self.bullet_mode == 0 else "BLUE",
            (
                self.player.curX - 12 + self.player.anim.animFlip * 10,
                self.player.curY - 5,
                COOLDOWN_RADIUS,
                COOLDOWN_RADIUS,
            ),
            0,
            (2 * math.pi * self.player.stamina / 100),
            4,
        )

    def updateShoot(self):
        if self.playermoves["shoot"]:
            mousepos = pygame.mouse.get_pos()
            pos = self.player.get_pos()
            pos = [
                pos[0] + 20 + (1 - self.player.anim.animFlip) * 30,
                pos[1] + 30,
            ]
            # sound play
            if self.bullet_mode == 0 and self.player.useStamina(99.9):
                self.shoot(mousepos, pos)
                sound.play("bullet1")
            elif self.bullet_mode == 1 and self.player.useStamina(33.3):
                self.shoot(mousepos, pos)
                sound.play("bullet2")
            if not conf.turbo:
                self.playermoves["shoot"] = False

    def shoot(self, mousepos, player_pos):
        vector = [mousepos[0] - player_pos[0], mousepos[1] - player_pos[1]]
        if self.bullet_mode == 0:
            self.shoot_bullet_1(player_pos, vector)
            self.hit_count.add_total(1)
        elif self.bullet_mode == 1:
            self.shoot_bullet_2(player_pos, vector)
            self.hit_count.add_total(3)

    def shoot_bullet_1(self, player_pos, vector):
        self.bullet_list.append(
            Bullet(
                player_pos,
                vector,
                self.bullet_mode,
                BULLET1_SPEED[self.level],
                BULLET1_DAMAGE[self.level],
            )
        )

    def shoot_bullet_2(self, player_pos, vector):
        for i in range(BULLET2_SHOOT_NUMS[self.level] // 2 + 1):
            if i == 0:
                self.shoot_bullet_2_util(player_pos, vector, 0)
            else:
                self.shoot_bullet_2_util(
                    player_pos, vector, BULLET2_SHOOT_ANGLE[self.level] * i
                )
                self.shoot_bullet_2_util(
                    player_pos, vector, -BULLET2_SHOOT_ANGLE[self.level] * i
                )

    def shoot_bullet_2_util(self, player_pos, vector, angel):
        new_vector = rotateVector(vector, angel)
        self.bullet_list.append(
            Bullet(
                player_pos,
                new_vector,
                self.bullet_mode,
                BULLET2_SPEED[self.level],
                BULLET2_DAMAGE[self.level],
            )
        )

    def generate_square(self):
        for i in range(random.randint(1, GENERATE_SQUARE[self.level])):
            self.enemiesGroup.add(
                Square(
                    size=[random.choice(SQUARE_SIZE)] * 2,
                    pos=[
                        random.randint(0, WIDTH),
                        random.randint(0, HEIGHT_UPPER_BOUND_SQUARE[self.level]),
                    ],
                    vector=[random.uniform(0, 1), random.uniform(0, 1)],
                    speed=random.randint(
                        SPEED_LOWER_BOUND_SQUARE[self.level],
                        SPEED_UPPER_BOUND_SQUARE[self.level],
                    ),
                    idx=random.randint(
                        INDEX_LOWER_BOUND_SQUARE[self.level],
                        INDEX_UPPER_BOUND_SQUARE[self.level],
                    ),
                )
            )

        self.scheduler.addJob(PERIOD_GENRATE[self.level], self.generate_square)

    def spawn_player(self):
        self.player = Player(
            WIDTH / 2 - PLAYER_SIZE[0] / 2, HEIGHT - 150 - PLAYER_SIZE[1] / 2, 300
        )
        self.playerGroup.add(self.player)

    def reset_game(self):
        # TODO
        # reset game
        pass

    def draw(self, deltaTime):
        """Draw and update the game"""
        self.screen.blit(self.background, (0, 0))

        # Player
        self.enemiesGroup.update(deltaTime)
        self.enemiesGroup.draw(self.screen)

        if self.playerGroup:
            self.player.update(deltaTime, self.playermoves, self.level)
            self.updateShoot()
            self.playerGroup.draw(self.screen)
            if not self.player.anim.slashDone:
                self.player.anim.swordSlashGroup.draw(self.screen)

        # Shield Player
        self.player.draw_shield(self.screen)

        # Cooldown
        self.draw_cooldown()

        # Bullet
        for bullet in self.bullet_list:
            bullet.update(self.screen)

        # Shield
        self.shields.draw(self.screen)

        # Score
        self.score.update(self.screen)

        # Timer
        self.timer.update(self.screen)

        # HitCount
        self.hit_count.update(self.screen)

        pygame.display.update()


if __name__ == "__main__":
    Game().begin()
