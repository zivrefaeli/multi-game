from enum import Enum

# General Constants
ROUND_NUMBERS = 2
SOURCE_FILE = 'source file'

class Data(Enum):
    ID = 'id'
    POS = 'position'
    COLOR = 'color'
    ANGLE = 'angle'
    HEALTH = 'health'
    BULLETS = 'bullets'

# Window Constants
WIDTH, HEIGHT = 500, 500 # px
FPS = 60

# Colors
BLACK = (0, 0, 0)
TRANSPARENT = (0, 0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

if __name__ == '__main__':
    filename = __file__.split('\\')[-1]
    print(f'{filename} {SOURCE_FILE}')