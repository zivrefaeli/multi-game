import socket

host = '0.0.0.0'
port = 3000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(('', 3000))

print(server.getsockname())

server.close()