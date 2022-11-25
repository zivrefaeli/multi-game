import pygame
from pygame import display, time, mouse, event, surface, image, font
from .ui import ClientUI
from .connection import ClientConnection
from objects import Json, Player, Clone, Bullet, Dot, WIDTH, HEIGHT, FPS, BLACK, WHITE 


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


def remove_locals(locals: dict[str, Clone], clients: dict[str, dict]) -> None:
    keys = []
    for key in locals:
        if key not in clients:
            keys.append(key)
    for key in keys:
        locals.pop(key)


def display_player_ammo(window: surface.Surface, ammo: int) -> None:
    BULLET = image.load('./assets/bullet.png')
    BULLET_DIMENTIONS = (4, 12)
    NUMBER_OF_BULLETS = 3
    AMMO_PER_BULLET = int(Player.MAX_AMMO / NUMBER_OF_BULLETS)
    AMMO_FONT = font.SysFont('Times', 16)
    PADDING = 10
    GAP = 2

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

        remove_locals(local_clones, connection.clones)

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
        
        display_player_ammo(window, player.ammo)

        player.display(window)
        display.update()

    pygame.quit()