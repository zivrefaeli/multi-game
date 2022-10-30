import pygame
from objects.constants import WIDTH, HEIGHT, WHITE
from objects.player import Player

def main():
    pygame.init()

    run = True
    window = pygame.display.set_mode((WIDTH, HEIGHT))

    p1 = Player('p1')
    p2 = Player('p2')
    p3 = Player('p3')

    p1.position.x += 100
    p2.position.y -= 50
    p3.position.x -= 35
    p3.position.y += 105

    while run:
        window.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        p1.display(window)
        p2.display(window)
        p3.display(window)
        
        pygame.display.update()

    pygame.quit()

if __name__ == '__main__':
    main()