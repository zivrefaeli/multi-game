import socket
from objects.methods import App
from objects.packet import *
from server import HandleClient, CloseSeverClient
from time import sleep

TARGET_ADDRESS = ('10.100.102.45', 1234)

def main() -> None:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect(TARGET_ADDRESS)
    except Exception as e:
        if type(e) == ConnectionRefusedError:
            print('server is closed')
        else:
            print(e)
        client.close()
        return

    id = input('Enter client id: ')

    App.send(client, Packet(ID_TYPE, id))

    response = App.receive(client)
    if response.type != ID_STATUS_TYPE:
        return
    status = response.data

    if status == HandleClient.VALID:
        
        count = 1
        while True:
            App.send(client, Packet('DATA', {'id': id, 'value': count}))
            db = App.receive(client)
            if db.type == ERROR_TYPE:
                break
            print(db.data)
            print('\n\n\n')
            count += 1
            sleep(1)

    else:
        print('invalid id')

    client.close()
    print('client closed')

if __name__ == '__main__':
    if int(input('1 - join server | 2 - close server ')) == 1:
        main()
    else:
        thread = CloseSeverClient(('10.100.102.45', 1234))
        thread.start()