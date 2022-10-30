import pygame
from pygame import display, time, mouse, event

def main() -> None:
    pygame.init()
    display.set_mode((WIDTH, HEIGHT), flags=pygame.HIDDEN)

    client_ui = ClientUI()
    client_ui.mainloop()
    if not client_ui.verified:
        pygame.quit()
        return

    connection = ClientConnection(client_ui.client, client_ui.id.get())
    connection.start()
    
    player = connection.player

    # UI settings
    display.set_caption(f'{player.id}`s screen')
    display.set_icon(player.icon)
    window = display.set_mode((WIDTH, HEIGHT), flags=pygame.SHOWN)
    clock = time.Clock()

    # TODO: create cloens dict and only update its values
    #       should not create a new client each frame
    # clones = dict()

    while connection.running:
        clock.tick(FPS)
        window.fill(WHITE)

        mx, my = mouse.get_pos()

        for e in event.get():
            if e.type == pygame.QUIT:
                connection.running = False
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

        for clone_id in connection.database:
            if clone_id == connection.id:
                continue
            clone_json = connection.database[clone_id]
            clone = Clone(clone_json)
            for position in clone_json[Data.BULLETS]:
                Bullet.draw(position, window)
            clone.display(window)
        
        player.rotate_to((mx, my))
        player.display(window)

        display.update()

    pygame.quit()

if __name__ == '__main__':
    main()