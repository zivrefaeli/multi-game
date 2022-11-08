import pygame
from pygame import time
from objects.constants import WIDTH, HEIGHT, WHITE
from objects.player import Player

def main():
    pygame.init()

    run = True
    window = pygame.display.set_mode((WIDTH, HEIGHT))

    p1 = Player('p1')
    clock = time.Clock()

    while run:
        clock.tick(60)
        window.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    p1.shoot()

        p1.display(window)

        pygame.display.update()

    pygame.quit()

if __name__ == '__main__':
    main()