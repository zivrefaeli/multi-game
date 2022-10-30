import socket

from server import BUFFER, CLOSE_ID

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect(('10.100.102.45', 1234))
except Exception as e:
    print(type(e))
    print(e)
else:
    client.send(input('enter id: ').encode())

    result = client.recv(BUFFER).decode()
    print(result)

client.close()