"""
NAMES: Larry Chiem, Ian Rowe, Raymond Shum, Nicholas Stankovich
DUE DATE: June 8, 2021
ASSIGNMENT: Team Programming Assignment #3
DESCRIPTION: This script was written for PYTHON 3. EC_server is a modification of server.
After both clients establish a connection, it allows for an unspecified number of messages
to be sent and received. User input sent from each client is relayed to the other and
displayed on the server console. One client can end the conversation for all parties by
sending the end phrase: "Bye". ECServer then terminates the connection to both clients.

For future implementation, we would look to have ECServer inherit the Server class and
override some of the existing methods.
"""
from socket import *
import threading


class ECServer:
    """
    EC_server allows two clients to send messages until one decides to end the chat
    by sending "Bye".
    """

    ordinal = {
        1: "first",
        2: "second"
    }  # Used for print formatting
    client_names = ["X", "Y"]  # Names of first and second connections
    total_clients = 2  # Number of expected clients
    end_phrase = "Bye"  # Used to close connections to all clients

    def __init__(self):
        self.serverPort = 12000
        self.hostname = '127.0.0.1'

        self.connections = []  # Holds established connections
        self.client_threads = []  # Used to cleanup client threads
        self.end_chat = False  # Tracks whether chat has ended

        self.serverSocket = socket(AF_INET, SOCK_STREAM)
        self.serverSocket.bind((self.hostname, self.serverPort))
        self.serverSocket.listen(1)

    def conn_handler(self):
        """
        Accepts connection requests from clients.
        """
        # Accepts connections until expected clients (two clients) are both connected.
        while len(self.connections) < self.total_clients:
            connectionSocket, addr = self.serverSocket.accept()

            # Each connection is stored in the order it was established
            self.connections.append(connectionSocket)
            index = self.connections.index(connectionSocket)

            # The first established client is "X" and the second is "Y"
            print("Accepted {0} connection, calling it client {1}".format(
                self.ordinal[index + 1],
                self.client_names[index]))

    def confirmation_msg(self, conn_list):
        """
        Sends message to clients, stating that connection is established.
        :param conn_list: Instance variable, connections
        """
        for client in conn_list:
            index = conn_list.index(client)
            msg = "[Server] Client {} has connected.".format(self.client_names[index])
            client.send(msg.encode())

    def recv_msg(self, connection):
        """
        Receives messages sent to "connection". Ends connection if message contains
        end phrase. Otherwise, formats and displays message to console.
        :param connection: connectionSocket object associated with a client
        """
        # Establishes client associated with the thread
        client_name = self.connections.index(connection)

        # Listens for messages while end phrase has not been sent by either client
        while not self.end_chat:
            msg = connection.recv(1024).decode()
            # Sends messages to both clients and prints to server console
            if msg:
                self.broadcast(msg, self.client_names[client_name])
                # If the message was also the end phrase, ends loop
                if msg == self.end_phrase:
                    self.end_chat = True

    def broadcast(self, msg, name="[Server]"):
        """
        Sends formatted message to all clients and prints to server console.
        :param msg: String to be broadcasted
        :param name: String representing name of originator of message
        """
        modified_msg = "{0}: {1}".format(name, msg)
        print(modified_msg)
        for client in self.connections:
            client.send(modified_msg.encode())

    def enable_client_communication(self):
        """
        Starts threads to receive messages for all established connections. Meant to be
        called after all clients are connected.
        """
        for client in self.connections:
            thread = threading.Thread(target=self.recv_msg, args=(client,))
            self.client_threads.append(thread)
            thread.start()

    def end_connections(self):
        """
        Sends notification to clients that Server will end their connection. Asks the
        clients to close their own connections. Joins threads and then closes connections.
        """
        for client in self.connections:
            client.send("[Server] Ended your connection.".encode())
            client.send(self.end_phrase.encode())

        for thread in self.client_threads:
            thread.join()

        for client in self.connections:
            client.close()

    def run(self):
        """
        Main function for EC_server.py.
        """

        # Server waits for both clients to connect and then sends confirmation messages
        print('The server is waiting to receive two connections....')
        self.conn_handler()
        self.confirmation_msg(self.connections)

        # Server begins to receive messages from clients.
        print("Waiting to receive messages from client X and client Y....")
        self.enable_client_communication()

        # Server waits until one client ends the chat
        while not self.end_chat:
            pass

        # Server ends connections with clients and joins threads
        print("Waiting a bit for clients to close their connections")
        self.end_connections()

        print("Done.")


if __name__ == "__main__":
    tcp_serv = ECServer()
    tcp_serv.run()
