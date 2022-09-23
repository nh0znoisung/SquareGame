GAME = "Square Game"
WIDTH, HEIGHT = (800, 600)
HEIGHT_UPPER_BOUND_SQUARE = 280

DATA_DIRNAME = "data"
FONT_FILENAME = "font.ttf"

SOUND_FILES = ("explode.ogg", "laser.ogg", "music.ogg", "title.ogg")

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

BAR_HEIGHT = 20

# BULLET_SIZE = (142, 82)
BULLET_SIZE = (17, 10)

SQUARE_POINT = [2, 5, 8, 10, 15, 25, 30, 40, 50]

# R1 = [x1, y1, x2, y2]
def isRectangleOverlap(R1, R2):
    if (R1[0] >= R2[2]) or (R1[2] <= R2[0]) or (R1[3] <= R2[1]) or (R1[1] >= R2[3]):
        return False
    else:
        return True


# point = [x, y]
# R = [x1, y1, x2, y2]
def isInsideRectangle(point, R):
    if point[0] >= R[0] and point[0] <= R[2] and point[1] >= R[1] and point[1] <= R[3]:
        return True
    else:
        return False
