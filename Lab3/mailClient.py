from socket import *
import base64
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText


def putCmd(clientSocket, cmd, args=""):
    """Send a command to the server."""
    if args == "":
        str = '%s%s' % (cmd, '\r\n')
    else:
        str = '%s %s%s' % (cmd, args, '\r\n')
    clientSocket.send(str.encode())


def doCmd(clientSocket, cmd, args=""):
    """Send a command, and return its response code."""
    putCmd(clientSocket, cmd, args)
    return clientSocket.recv(1024).decode()


msg = "\r\n I love computer networks!"
END_MSG = "\r\n."

gmail_user = 'minh00012258@gmail.com'
gmail_password = 'iyijgsyrokenbxcu'

# Choose a mail server (e.g. Google mail server) and call it mailServer
mailServer = ("smtp.gmail.com", 587)

# Create socket called clientSocket and establish a TCP connection with mailServer
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(mailServer)
print(clientSocket.recv(1024).decode())


# Send EHLO command and print server response.
print(doCmd(clientSocket, 'EHLO', 'smtp.gmail.com'))

# Start TLS
print(doCmd(clientSocket, 'STARTTLS'))


context = ssl.create_default_context()
clientSocket = context.wrap_socket(clientSocket, server_hostname="smtp.gmail.com")


bytes_str = ("\x00"+gmail_user+"\x00"+gmail_password).encode()
base64_str = base64.b64encode(bytes_str)
sendAuth = "AUTH PLAIN ".encode() + base64_str + "\r\n".encode()
clientSocket.send(sendAuth)
print(clientSocket.recv(1024).decode())

# Send MAIL FROM command and print server response.
print(doCmd(clientSocket, 'MAIL', 'FROM:<minh00012258@gmail.com>'))

# Send RCPT TO command and print server response.
print(doCmd(clientSocket, 'RCPT', 'TO:<minh00012258@gmail.com>'))

# Send DATA command and print server response.
print(doCmd(clientSocket, 'DATA'))

# # Send message data.
# clientSocket.send(msg.encode())

# Send image data
msgRoot = MIMEMultipart()

txt = MIMEText('<b>%s</b><br><img src="cid:%s"><br>' % ("abcxy", 'moon.jpg'), 'html')
msgRoot.attach(txt)

f = open('moon.jpg', 'rb')
img = MIMEImage(f.read())
f.close()
img.add_header('Content-ID', '<moon.jpg>')
msgRoot.attach(img)

print(msgRoot)

print(clientSocket.send(msgRoot.as_string().encode()))

# Message ends with a single period.
print(doCmd(clientSocket, END_MSG))

# Send QUIT command and get server response.
print(doCmd(clientSocket, 'QUIT'))

clientSocket.close()
