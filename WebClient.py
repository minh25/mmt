import sys
from socket import *




if __name__ == '__main__':
    args = sys.argv[1:]
    print(args)

    serverName = args[0]
    serverPort = int(args[1])

    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))

    clientSocket.sendall(b"GET /index.html HTTP/1.1\r\nHost: 192.168.1.15:1251\r\nAccept: text/html\r\n\r\n")

    data = clientSocket.recv(4096)
    print('From Server:', data.decode())

    clientSocket.close()