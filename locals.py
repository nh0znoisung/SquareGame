import math
import sys

GAME = 'Square Game'
# WIDTH, HEIGHT = (800, 600)
WIDTH, HEIGHT = (600, 800)


DATA_DIRNAME = "data"
FONT_FILENAME = "font.ttf"

SOUND_FILES = (
    "explode.wav",
    "laser.ogg",
    "music.mp3",
    "title.mp3",
    "die.wav",
    "slash.wav",
    "dash.wav",
    "menu_choosing.wav",
    "menu_picked.wav",
    "menu_switch.wav",
    "bullet1.mp3",
    "bullet2.wav",
    "shield.wav"
)

BACKGROUND = (0x11, 0x11, 0x00)
WHITE = (0xFF, 0xFF, 0xFF)
BLACK = (0x00, 0x00, 0x00)

# BACKGROUND = WHITE
TRANSPARENT = BLACK

HIGHSCORES_AMOUNT = 10

FRAME_RATE = 60
MENU_FRAME_RATE = 24

PLAYER_SIZE = (100, 100)
DELTA_PLAYER_SIZE = 15

SHIELD_SIZE = [37.5, 45]
SHIELD_MAX_NUMS = 3
SHIELD_COOLDOWN = 10
SHIELD_PROTECT = 3
SHIELD_DELTA_SPACE = 10

WIDTH_BAR = 20
SCORE_BAR_HEIGHT = 20
TIMER_BAR_HEIGHT = 45

BULLET1_SIZE = (17, 10)
BULLET2_SIZE = (25, 20)
BULLET_TYPE_NUMS = 2

COOLDOWN_RADIUS = 110

# Setup level
SQUARE_SIZE = [50, 60, 70, 80, 95]
SQUARE_POINT = [25,35,45,55,70,95,120,150,200] 
LEVEL_SCORE_UPPER_BOUND = [100, 400, 1000, sys.maxsize]
LEVEL_NUMS = 4
HEIGHT_UPPER_BOUND_SQUARE = [220,255,385,325]
SPEED_LOWER_BOUND_SQUARE = [100, 150, 200, 225]
SPEED_UPPER_BOUND_SQUARE = [150, 200, 225, 250]
INDEX_LOWER_BOUND_SQUARE = [0,1,3,5]
INDEX_UPPER_BOUND_SQUARE = [2,4,6,8]
PERIOD_GENRATE = [8.5,8,7,6]
BULLET1_DAMAGE = [3,4,6,9]
BULLET1_SPEED = [6,8,10,13]
BULLET1_COOLDOWN = [1.5,1.2,1,0.8]
BULLET2_DAMAGE = [1,3,4,6]
BULLET2_SHOOT_NUMS = [3,3,3,5] #odd number
BULLET2_SHOOT_ANGLE = [30,30,20,16] #degree
BULLET2_SPEED = [4,6,8,10]
GENERATE_SQUARE = [1,2,3,5]
SLASH_DAMAGE = [0.2, 0.35, 0.6, 0.9]

black = (0,0,0)
white = (255,255,255)

red = (200,0,0)
green = (0,200,0)

bright_red = (255,0,0)
bright_green = (0,255,0)

INPUT_WIDTH = 380
INPUT_HEIGHT = 32

# R1 = [x1, y1, x2, y2]
def isRectangleOverlap(R1, R2):
    if (R1[0] >= R2[2]) or (R1[2] <= R2[0]) or (R1[3] <= R2[1]) or (R1[1] >= R2[3]):
        return False
    else:
        return True


# point = [x, y]
# R = [x1, y1, x2, y2]
def isInsideRectangle(point, R):
    if (point[0]>=R[0] - 10 and point[0]<=R[2] and point[1]>=R[1] - 20 and point[1]<=R[3]):
        return True
    else:
        return False

def rotateVector(vector, angle, rad = False):
    if not rad:
        angle = math.radians(angle)
    return [vector[0]*math.cos(angle) - vector[1]*math.sin(angle), vector[0]*math.sin(angle) + vector[1]*math.cos(angle)]
