import server, client
valid = ['server', 'client']

debug = input('>>> ')
while debug not in valid:
    debug = input('>>> ')

if debug == valid[0]:
    server.smain()
else:
    client.cmain()