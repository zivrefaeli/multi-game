import pygame
from pygame import time, mouse, display
from objects import Player, WIDTH, HEIGHT, WHITE


def main():
    pygame.init()

    run = True
    window = display.set_mode((WIDTH, HEIGHT))

    player = Player()
    display.set_icon(player.icon)
    display.set_caption(f'{player.id} screan')

    clock = time.Clock()

    enemy = Player('Enemy')
    enemy.angle = 30

    while run:
        clock.tick(60)
        window.fill(WHITE)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False
                break

            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_w:
                    player.accelerating = True
                    player.moving = True
                
                elif e.key == pygame.K_LSHIFT:
                    player.crouching = True
            
            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_w:
                    player.accelerating = False
                
                elif e.key == pygame.K_LSHIFT:
                    player.crouching = False

            elif e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1:
                    player.shooting = True
                elif e.button == 3:
                    player.shoot()
            
            elif e.type == pygame.MOUSEBUTTONUP:
                if e.button == 1:
                    player.shooting = False
        
        player.rotate_to(mouse.get_pos())

        if player.shooting:
            player.shoot()

        if player.hit(enemy.position, enemy.angle):
            enemy.health -= 1

        enemy.display(window)
        player.display(window)
        
        display.update()

    pygame.quit()


if __name__ == '__main__':
    main()