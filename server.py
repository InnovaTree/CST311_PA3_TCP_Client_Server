# TCPCapitalizationServer.py
from socket import *
import threading

serverPort = 12000

# Create a TCP socket
# Notice the use of SOCK_STREAM for TCP packets
serverSocket = socket(AF_INET, SOCK_STREAM)

# Assign IP address and port number to socket
serverSocket.bind(('127.0.0.1', serverPort))
serverSocket.listen(1)

print('The server is waiting to receive two connections....')

connections = []
client_names = ["X", "Y"]
rcvd_msgs = []
# Add list to hold threads

ordinal = {
    1: "first",
    2: "second"
}


def confirmation_msg(conn_list):
    for client in conn_list:
        msg = "Client {} has connected.".format(client_names[conn_list.index(client)])
        client.send(msg.encode())


def recieve(connection):
    while True:
        msg = connection.recv(1024)
        if msg:
            print("[DEBUG] From Client {0}: {1}".format(client_names[connections.index(connection)], msg.decode()))
            rcvd_msgs.append((connections.index(connection), msg.decode()))


while len(connections) < 2:
    connectionSocket, addr = serverSocket.accept()
    connections.append(connectionSocket)

    index = connections.index(connectionSocket)
    print("Accepted {0} connection, calling it client {1}.".format(ordinal[index + 1], client_names[index]))

confirmation_msg(connections)
print("Waiting to receive messages from client X and client Y....")

for client in connections:
    thread = threading.Thread(target=recieve, args=(client,))
    thread.start()

while len(rcvd_msgs) < 2:
    pass

for index, msg in rcvd_msgs:
    print("Client {0} sent message {1}: {2}".format(client_names[index], rcvd_msgs.index((index, msg)) + 1, msg))

""" Need to unpack tuples
for client in connections:
    message = "{}: {} received before {}: {}".format()
"""

# Remember to join threads
# Remember to close connections
