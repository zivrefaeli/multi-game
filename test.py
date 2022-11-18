import pygame
from pygame import time, mouse, display
from objects import *
from math import sqrt, degrees, atan, cos, sin, radians

R_MAX = sqrt(2) / 2 * Player.SIZE

def hitbox(bullet: Dot, clone: Dot, angle: int) -> bool:
    # relative dot (a, b) to clone position as origin
    a = bullet.x - clone.x
    b = bullet.y - clone.y
    r = sqrt(a ** 2 + b ** 2)

    try:
        alpha = degrees(atan(b / a))
    except ZeroDivisionError:
        alpha = 90 if b > 0 else 270
    
    j = alpha - angle
    beta = radians(j)
    x, y = round(r * cos(beta)), round(r * sin(beta))
    d = Player.SIZE / 2

    return -d <= x <= d and -d <= y <= d


def main():
    pygame.init()

    run = True
    window = display.set_mode((WIDTH, HEIGHT))

    player = Player()
    display.set_icon(player.icon)
    display.set_caption(f'{player.id} screan')

    clock = time.Clock()

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
        
        if player.shooting:
            player.shoot()

        player.rotate_to(mouse.get_pos())
        player.display(window)
        
        display.update()

    pygame.quit()


if __name__ == '__main__':
    main()