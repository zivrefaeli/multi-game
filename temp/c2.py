import socket, sys
from threading import Thread
from methods import App, Packet

import pygame
from constants import *
from player import Player, PlayerClone

HOST = socket.gethostbyname(socket.gethostname())
ADDR = (HOST, App.PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
left = False
run = True

clone_players = []

# TODO: update exsiting clones, and remove clones if they removed/left server

def convert_data(username: str, server_packet: Packet) -> list:
    clones = []
    server_data = server_packet.data

    for key in server_data:
        value = server_data[key]

        if key != username:
            clones.append(PlayerClone(value))
    return clones            

def game_ui(username) -> None:
    global run, left

    pygame.init()
    pygame.display.set_caption(f'{username}`s screen')

    window = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    player = Player(name=username)

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
                    player.shooting = True

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    player.shooting = False
        
        player.rotate(mouse)
        player.draw(window)

        if run:
            App.send(client, Packet('client-data', player.get_player_data()))
            for clone in clone_players:
                clone.draw(window)

        pygame.display.update()

    pygame.quit()

    left = True
    App.send(client, Packet('client-left', 'LEFT'))

def main() -> None:
    try:
        client.connect(ADDR)
    except ConnectionRefusedError:
        print('server is closed')
        client.close()
        return
    
    uname = input('enter username: ')
    App.send(client, uname)
    while App.receive(client) == 'bad-username':
        uname = input('enter username: ')
        App.send(client, uname)

    Thread(target=game_ui, args=(uname,)).start()

    server_data = App.receive(client)
    global clone_players, run

    while server_data.type != 'server-closed' and not left:
        clone_players = convert_data(uname, server_data)
        if run:
            server_data = App.receive(client)

    if not left:
        run = False
        print('server closed')

    client.close()

if __name__ == '__main__':
    main()