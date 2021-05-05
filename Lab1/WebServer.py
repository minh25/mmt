from socket import *
import time
import threading

serverPort = 1260
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen()


def socketThread(connectionSocket, address):
    # time.sleep(10)
    try:
        print(connectionSocket, address)

        message = connectionSocket.recv(1024)

        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()

        string = "HTTP/1.1 200 OK\n" + "Content-Type: text/html\n" + "\n"
        for i in range(0, len(outputdata)):
            string += outputdata[i]
        string += "\r\n"

        connectionSocket.send(string.encode())

        print("OK")
        connectionSocket.close()

    except IOError:
        connectionSocket.send("HTTP/1.1 404 Not Found\n\n".encode())
        print("ERROR")
        connectionSocket.close()


if __name__ == '__main__':

    threads = list()

    while True:
        print('Ready to serve...')
        connectionSocket, address = serverSocket.accept()

        thread = threading.Thread(target=socketThread, args=(connectionSocket, address,), daemon=None)
        threads.append(thread)
        thread.start()

        for thread in threads:
            if not thread.is_alive():
                threads.remove(thread)

        print(len(threads))

    serverSocket.close()
