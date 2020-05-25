from socket import *

Host = ''
Port = 13144
Bufsize = 1024
Addr = (Host, Port)

tcp = socket(AF_INET, SOCK_STREAM)
tcp.bind(Addr)
tcp.listen(5)

while True:
    print('waiting for connection...')
    client, addr = tcp.accept()
    print('...connected from:', addr)

    while True:
        data = client.recv(Bufsize)
        if not data:
            break
        client.send(data)
    client.close()

tcp.close()
