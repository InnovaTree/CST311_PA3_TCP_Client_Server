"""
Header

Threading: Necessary because input() is a blocking function. While client is waiting for
user input, server could have sent a message. This allows threads to receive and send
messages to be run concurrently.
"""

from socket import *
import threading


class Client:
    """
    Client establishes a TCP connection with Server, waits for connection to be confirmed,
    sends a message to client,
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
