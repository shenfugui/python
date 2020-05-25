from socket import *

Host = '47.106.174.15'
Port = 39888
Bufsize = 1024
Addr = (Host, Port)

tcp = socket(AF_INET, SOCK_STREAM)
tcp.connect(Addr)

while True:
    data = input('> ')
    if not data:
        break
    tcp.send(data.encode('utf-8'))
    data = tcp.recv(Bufsize)
    if not data:
        break
    print(data.decode('utf-8'))

tcp.close()