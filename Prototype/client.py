"""
NAMES: Larry Chiem, Ian Rowe, Raymond Shum, Nicholas Stankovich
DUE DATE: June 8, 2021
ASSIGNMENT: Team Programming Assignment #3
DESCRIPTION: This script was written for PYTHON 3. Client receives and sends messages
in sequential order, without the use of threads. It connects to the server and waits for
a confirmation message. It then allows the user to input a message to send to the server.
It waits to receive a response detailing the contents and order of messages received by
the server from both connected clients. Then it closes its connection.
"""

from socket import *


class Client:
    """
    Client establishes a TCP connection with Server, waits for connection to be confirmed,
    sends a message to server and waits for the response.
    """

    def __init__(self):
        self.serverName = '127.0.0.1'
        self.serverPort = 12000

        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.clientSocket.connect((self.serverName, self.serverPort))

    def run(self):
        """
        Main function for client.py
        """

        # Waits for connection establishment confirmation message from server and prints
        print(self.clientSocket.recv(1024).decode())

        # Accepts user input and sends message to server
        sentence = input('Enter message to send to server: ')
        self.clientSocket.send(sentence.encode())

        # Waits for response detailing message receipt order from server and prints
        print(self.clientSocket.recv(1024).decode())

        # Closes connection
        self.clientSocket.close()


if __name__ == "__main__":
    tcp_client = Client()
    tcp_client.run()
