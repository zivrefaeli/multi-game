import pygame
from pygame import time, mouse
from objects.constants import WIDTH, HEIGHT, WHITE
from objects.player import Player
from objects.health_bar import HealthBar
from objects.dot import Dot
from objects.methods import Methods
from math import sqrt, degrees, atan, cos, sin, radians

R_MAX = sqrt(2) / 2 * Player.SIZE

def hitbox(bullet: Dot, clone: Dot, angle: int) -> tuple[bool, float]:
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

    return -d <= x <= d and -d <= y <= d, j

def radius(b: Dot, c: Dot) -> bool:
    return R_MAX >= ((b.x - c.x) ** 2 + (b.y - c.y) ** 2) ** 0.5

def main():
    pygame.init()

    run = True
    window = pygame.display.set_mode((WIDTH, HEIGHT))

    p1 = Player('Moshe')
    clock = time.Clock()
    c = Methods.random_color()

    p2 = Player('ziv')
    # p2.angle = 33
    p2.position.x = 60
    p2.position.y = 100

    while run:
        clock.tick(60)
        window.fill(WHITE)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False
                break

            # elif event.type == pygame.MOUSEBUTTONDOWN:
            #     if event.button == 1:
            #         p1.shoot()

            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_w:
                    p1.accelerating = True
                    p1.moving = True
                
                elif e.key == pygame.K_LSHIFT:
                    p1.crouching = True
            
            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_w:
                    p1.accelerating = False
                
                elif e.key == pygame.K_LSHIFT:
                    p1.crouching = False

            elif e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1:
                    p1.shooting = True
                elif e.button == 3:
                    p1.shoot()
            
            elif e.type == pygame.MOUSEBUTTONUP:
                if e.button == 1:
                    p1.shooting = False
        
        if p1.shooting:
            p1.shoot()

        p1.rotate_to(mouse.get_pos())
        p1.display(window)

        p2.display(window)
        attack = 0
        i = 0
        while i < len(p1.bullets):
            b = p1.bullets[i]
            if radius(b.position, p2.position):
                print('in')
                x = hitbox(b.position, p2.position, p2.angle)
                if x[0]:
                    attack += 1
                    p1.bullets.pop(i)
                    print('V', x[1])
                    continue
            i += 1

        p2.health -= attack * 5
        if p2.health < 0:
            p2.health = Player.FULL_HEALTH

        
        pygame.display.update()

    pygame.quit()

if __name__ == '__main__':
    main()