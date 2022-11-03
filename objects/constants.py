# General Constants
ROUND_NUMBERS = 2
SOURCE_FILE = 'source file'

# Player Constants
PLAYER_SIZE = 50 #px
ID_DELTA = 40 #px
CLIENT_DATA = 'DATA'

# Window Constants
WIDTH, HEIGHT = 500, 500 #px
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

if __name__ == '__main__':
    filename = __file__.split('\\')[-1]
    print(f'{filename} {SOURCE_FILE}')