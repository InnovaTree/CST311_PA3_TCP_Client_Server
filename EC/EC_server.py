"""
To be done:

"""

# TCPCapitalizationServer.py
from socket import *
import threading


class Server():

    def __init__(self):
        self.serverPort = 12000
        self.serverSocket = socket(AF_INET, SOCK_STREAM)
        self.serverSocket.bind(('127.0.0.1', self.serverPort))
        self.serverSocket.listen()

        self.client_connections = []
        self.client_names = []

    def conn_handler(self):
        while True:
            connectionSocket, addr = self.serverSocket.accept()
            self.client_connections.append(connectionSocket)
            client_name = connectionSocket.recv(1024).decode()
            self.client_names.append(client_name)

            notification_msg = "{0} has connected as {1}.".format(addr, client_name)
            self.broadcast(notification_msg)

            thread = threading.Thread(target=self.recv_msg, args=(connectionSocket,))
            thread.start()

    def recv_msg(self, client):
        client_name = self.client_names[self.client_connections.index(client)]
        while True:
            msg = client.recv(1024).decode()
            if msg:
                self.broadcast(msg, client_name)

    def broadcast(self, msg, name="[Server]"):
        modified_msg = "{0}: {1}".format(name, msg)
        print(modified_msg)
        for client in self.client_connections:
            client.send(modified_msg.encode())

    def start(self):
        self.conn_handler()


if __name__ == "__main__":
    chat_serv = Server()
    chat_serv.start()
