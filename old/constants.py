import pygame

pygame.init()

# float Values: (round-2)
# Dot.x | Dot.y | Vector.size

# int Values:
# Vector.angle


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

WIDTH, HEIGHT = 800, 600
ICON_SIZE = (32, 32)
FPS = 80
BG_COLOR = WHITE

PLAYER_DEFAULT_SIZE = 50
PLAYER_DEFAULT_SPEED = .5
BULLET_DEFAULT_SPEED = 3
PLAYER_NAME_FONT = pygame.font.SysFont('Calibri', 16)
PLAYER_NAME_DELTA = PLAYER_DEFAULT_SIZE * .9

if __name__ == '__main__':
    file_name = __file__.split('\\')[-1]
    print(f'{file_name} is a source file')