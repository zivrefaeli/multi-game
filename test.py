import pygame
from pygame import time, mouse, display
from objects import Player, WIDTH, HEIGHT, WHITE, FPS
from client.main import display_player_ammo


def handle_events(player: Player) -> bool:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            return False

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
    return True


def main():
    pygame.init()

    run = True
    window = display.set_mode((WIDTH, HEIGHT))

    player = Player()
    display.set_icon(player.icon)
    display.set_caption(f'{player.id}\'s screen')

    clock = time.Clock()

    enemy = Player('Enemy')
    enemy.angle = 30

    while run:
        clock.tick(FPS)
        window.fill(WHITE) 

        run = handle_events(player)
        
        player.rotate_to(mouse.get_pos())
        if player.shooting:
            player.shoot()
        
        if player.hit(enemy.position, enemy.angle):
            enemy.health -= 1
            if enemy.health <= 0:
                enemy.health = Player.FULL_HEALTH

        enemy.display(window)
        display_player_ammo(window, player.ammo)
        player.display(window)
        
        display.update()

    pygame.quit()


if __name__ == '__main__':
    main()