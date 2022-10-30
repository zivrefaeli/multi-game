import socket

DB = {'Moshe': '1+1=2'}
conceted = []

machine_ip = socket.gethostbyname(socket.gethostname())
port = 3000

print(f'IP Address: {machine_ip}:{port}')

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((machine_ip, port))

server.listen(3)
print('The server is listening')

client, client_address = server.accept()
print(f'client joined from {client_address}')

client_id = client.recv(2048).decode()

valid = 'valid' if not client_id in DB else 'invalid'

client.send(valid.encode())

if valid == 'valid':
    status = client.recv(2048).decode()
    DB[client_id] = status
    print('current DB is', DB)
else:
    print('invalid id')

server.close()
print('server closed')