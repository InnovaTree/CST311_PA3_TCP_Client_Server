# TCPCapitalizationServer.py
from socket import *

serverPort = 12000

# Create a TCP socket
# Notice the use of SOCK_STREAM for TCP packets
serverSocket = socket(AF_INET, SOCK_STREAM)

# Assign IP address and port number to socket
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

print('The server is ready to receive')

connections = []
while len(connections) < 2:
    connectionSocket, addr = serverSocket.accept()
    connections.append((connectionSocket,addr))
    print("Client {0} has connected".format(len(connections)))
    # server needs to associate handler thread with each client



""" From base code
while True:
    sentence = connectionSocket.recv(1024).decode()
    capitalizedSentence = sentence.upper()
    connectionSocket.send(capitalizedSentence.encode())
    connectionSocket.close()
"""