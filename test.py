import pygame
from pygame import time, mouse, display, surface, image, font
from objects import Player, Dot, WIDTH, HEIGHT, WHITE, BLACK

def display_player_ammo(window: surface.Surface, ammo: int) -> None:
    NUMBER_OF_BULLETS = 3
    BULLET_DIMENTIONS = (4, 12)
    PADDING = 10
    GAP = 2
    AMMO_FONT = font.SysFont('Times', 16)
    AMMO_PER_BULLET = int(Player.MAX_AMMO / NUMBER_OF_BULLETS)
    BULLET = image.load('./assets/bullet.png')

    dot = Dot(PADDING, HEIGHT - PADDING)
    bullets = ammo // AMMO_PER_BULLET + int(ammo % AMMO_PER_BULLET != 0)
    
    ammo_text = AMMO_FONT.render(f'{ammo}/{Player.MAX_AMMO}', True, BLACK)
    text_rect = ammo_text.get_rect(bottomleft=dot.get())

    window.blit(ammo_text, text_rect)

    dot.x += text_rect.width + PADDING
    dot.y -= text_rect.height / 2

    for _ in range(bullets):
        window.blit(BULLET, BULLET.get_rect(midleft=dot.get()))
        dot.x += BULLET_DIMENTIONS[0] + GAP


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
        
        m = mouse.get_pos()
        # print(m)
        player.rotate_to(m)

        if player.shooting:
            player.shoot()

        if player.hit(enemy.position, enemy.angle):
            enemy.health -= 1

        enemy.display(window)

        display_player_ammo(window, player.ammo)

        player.display(window)
        
        display.update()

    pygame.quit()


if __name__ == '__main__':
    main()