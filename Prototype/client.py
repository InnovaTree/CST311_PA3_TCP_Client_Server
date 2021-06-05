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
    end_phrase = "Bye"

    def __init__(self):
        self.serverName = '127.0.0.1'
        self.serverPort = 12000
        self.msg_recvd = False  # Tracks whether first message has been received from Server

        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.clientSocket.connect((self.serverName, self.serverPort))

    def recv_msg(self):
        """
        Receives messages sent from server. Ends connection if message contains "Bye". Else,
        it displays the received message.
        """
        # Waits on an infinite loop to receive messages
        while True:
            msg = self.clientSocket.recv(1024).decode()
            # Ends connection if message contains "Bye"
            if msg == self.end_phrase:
                self.clientSocket.send(self.end_phrase.encode())
                self.clientSocket.close()
                break
            # Else, displays message to console
            elif msg:
                print(msg)
                self.msg_recvd = True

    def run(self):
        """
        Main function for client.py
        """
        # Starts a thread to receive messages from server.
        thread = threading.Thread(target=self.recv_msg)
        thread.start()

        # Waits for connection establishment message from server
        while not self.msg_recvd:
            pass

        # Accepts user input and sends message to server
        sentence = input('Enter message to send to server: ')
        self.clientSocket.send(sentence.encode())

        # Do we need to wait for response here?
        thread.join()


if __name__ == "__main__":
    tcp_client = Client()
    tcp_client.run()
