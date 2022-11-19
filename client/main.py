import pygame
from pygame import display, time, mouse, event
from .ui import ClientUI
from .connection import ClientConnection
from objects import Json, Player, Clone, Bullet, WIDTH, HEIGHT, FPS, WHITE


def handle_events(connection: ClientConnection, player: Player) -> None:
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


# delete clients which left the server
def remove_clients(locals: dict[str, Clone], clients: dict[str, dict]) -> None:
    pops = []
    for key in locals.keys():
        if key not in clients:
            pops.append(key)
    for key in pops:
        locals.pop(key)


def cmain() -> None:
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

    display.set_caption(f'{player.id}\'s screen')
    display.set_icon(player.icon)
    window = display.set_mode((WIDTH, HEIGHT), flags=pygame.SHOWN)
    clock = time.Clock()

    local_clones: dict[str, Clone] = dict()

    while connection.running:
        clock.tick(FPS)
        window.fill(WHITE)

        handle_events(connection, player)
        
        player.rotate_to(mouse.get_pos())
        if player.shooting:
            player.shoot()

        # remove_clients(local_clones, connection.clones)

        for clone_id in connection.clones:
            if clone_id == connection.id:
                continue
            clone_json = connection.clones[clone_id]
            
            # display clones' bullets
            for position in clone_json[Json.BULLETS]:
                Bullet.draw(window, clone_json[Json.COLOR], position)
            
            # display clones
            if not clone_id in local_clones:
                local_clones[clone_id] = Clone(clone_json)
            else:
                local_clones[clone_id].update_json(clone_json)
            local_clones[clone_id].display(window)
        
        player.display(window)
        display.update()

    pygame.quit()