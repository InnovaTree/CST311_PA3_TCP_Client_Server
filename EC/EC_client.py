"""

"""

from socket import *
import threading


def recv_msg(clientSocket):
    while True:
        msg = clientSocket.recv(1024).decode()
        if msg:
            print(msg)


def send_msg(clientSocket):
    while True:
        clientSocket.send(input("").encode())


# In your command prompt, type in hostname and press enter.
# What comes up is your computer's hostname
serverName = '127.0.0.1'
serverPort = 12000

client_name = input("Please enter your name: ")

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
clientSocket.send(client_name.encode())
threads = []
threads.append(threading.Thread(target=recv_msg, args=(clientSocket,)))
threads.append(threading.Thread(target=send_msg, args=(clientSocket,)))

for thread in threads:
    thread.start()
