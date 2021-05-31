"""

"""

from socket import *
import threading

# In your command prompt, type in hostname and press enter.
# What comes up is your computer's hostname
serverName = '127.0.0.1'
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

msg_recvd = False


def recv_msg():
    while True:
        msg = clientSocket.recv(1024).decode()
        if msg == "Bye":
            clientSocket.send("Bye".encode())
            clientSocket.close()
            break
        elif msg:
            print(msg)
            global msg_recvd
            msg_recvd = True


thread = threading.Thread(target=recv_msg)
thread.start()

while not msg_recvd:
    pass

sentence = input('Enter message to send to server: ')
clientSocket.send(sentence.encode())

thread.join()
