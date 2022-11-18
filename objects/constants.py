# General Constants
ROUND_NUMBERS = 2

# Window Constants
WIDTH, HEIGHT = 500, 500 # px
FPS = 60

# Colors
BLACK = (0, 0, 0)
TRANSPARENT = (0, 0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)


def source_file(file: str) -> None:
    filename = file.split('\\')[-1]
    print(f'{filename} source file')


if __name__ == '__main__':
    source_file(__file__)