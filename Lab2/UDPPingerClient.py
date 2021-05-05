import random
from socket import *
import datetime

serverName = "172.20.10.2"
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_DGRAM)

totalMessage = 20
lossMessage = 0

timeOut_s = 1

for i in range(totalMessage):
    try:
        message = str(i)

        clientSocket.settimeout(timeOut_s)
        aTime = datetime.datetime.now()
        clientSocket.sendto(message.encode(), (serverName, serverPort))
        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
        bTime = datetime.datetime.now()

        newMessage = modifiedMessage.decode()

        print("Ping", serverName, (bTime - aTime).microseconds, "ms")
    except timeout as e:
        print("Ping", serverName, "timeout")
        lossMessage += 1

clientSocket.close()

print()
print("Time out:", timeOut_s, "s")
print("Loss rate:", lossMessage/totalMessage*100, "%")