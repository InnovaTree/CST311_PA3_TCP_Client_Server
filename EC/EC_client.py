"""
NAMES: Larry Chiem, Ian Rowe, Raymond Shum, Nicholas Stankovich
DUE DATE: June 8, 2021
ASSIGNMENT: Team Programming Assignment #3
DESCRIPTION: This script was written for PYTHON 3.
"""

from socket import *
import threading


class EC_client:
    """
    EC_client establishes a connection with the server, then allows messages to be
    relayed to an from another EC_client until one party ends the chat.
    """

    end_phrase = "Bye"  # Used to end the chat

    def __init__(self):

        self.serverName = '127.0.0.1'
        self.serverPort = 12000
        self.end_chat = False

        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.clientSocket.connect((self.serverName, self.serverPort))

    def recv_msg(self):
        """
        Receives messages from the server and prints to console until end phrase is
        received.
        """
        while not self.end_chat:
            msg = self.clientSocket.recv(1024).decode()
            # Does not display end phrase from server but ends loop if received
            if msg == self.end_phrase:
                self.end_chat = True
            # Will receive modified end phrase from client, relayed through server
            elif msg:
                print(msg)

    def send_msg(self):
        """
        Asks for user input and sends messages to server on a loop.
        """
        while True:
            msg = input("")
            self.clientSocket.send(msg.encode())


    def run(self):

        # send_msg is started as a daemon thread (input is blocking), will end with program
        # EC_server will not receive messages until both clients are connected
        thread = threading.Thread(target=self.send_msg, daemon=True)
        thread.start()

        # Listens for messages relayed from server until end_phrase is received
        self.recv_msg()

        self.clientSocket.close()


if __name__ == "__main__":
    tcp_client = EC_client()
    tcp_client.run()
