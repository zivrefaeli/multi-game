import pygame
from constants import *
from objects import Player, PlayerClone

# TODO: fix func at objects (hit-box)
# TODO: create server-client UIs

def main(title: str = 'App') -> None:
    pygame.init()
    pygame.display.set_caption(title)

    window = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    run = True

    player = Player()
    clone = PlayerClone(player.get_player_data())
    clone.name += ' clone'
    clone.angle = 30

    # icon = client's skin
    icon = pygame.transform.scale(player.skin, ICON_SIZE) 
    pygame.display.set_icon(icon)

    while run:
        clock.tick(FPS)
        window.fill(BG_COLOR)
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player.accelerating = True
                    player.moving = True
                
                elif event.key == pygame.K_LSHIFT:
                    player.crouching = True
            
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    player.accelerating = False
                
                elif event.key == pygame.K_LSHIFT:
                    player.crouching = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    player.shoot()

            # elif event.type == pygame.MOUSEBUTTONUP:
            #     if event.button == 1:
            #         player.shooting = False
        
        player.rotate(mouse)

        clone.draw(window)
        
        player.draw(window)

        player.hit([clone])

        pygame.display.update()

    pygame.quit()

if __name__ == '__main__':
    main('multi-game')