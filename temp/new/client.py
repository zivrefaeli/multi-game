import socket

ID = 'Moshe'
STATUS = '1+1=2'

target_ip = '10.100.102.45'
target_port = 1234

print(f'Target IP Address: {target_ip}:{target_port}')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((target_ip, target_port))

client.send(ID.encode())

is_valid_id = client.recv(2048).decode()

if is_valid_id == 'valid':
    client.send(STATUS.encode())
    print(f'status ({STATUS}) sent')
else:
    print('id already exists in server`s DB')

client.close()
print('client connection closed')