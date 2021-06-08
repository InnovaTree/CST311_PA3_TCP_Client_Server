"""
NAMES: Larry Chiem, Ian Rowe, Raymond Shum, Nicholas Stankovich
DUE DATE: June 8, 2021
ASSIGNMENT: Team Programming Assignment #3
DESCRIPTION: This script was written for PYTHON 3. Server accepts TCP connections from
two clients before receiving messages. It notifies both clients that they've connected,
and waits for messages to be sent from both clients. It prints received messages in the
console windows and sends a formatted to each client, acknowledging the order of receipt.

20. Multithreading.
    The server script needed to implement multithreading in order to listen for
    incoming messages from multiple clients. Unlike UDP, which receives messages
    on the same port, this server script opens TCP connections with its clients
    whose resulting ports are unique.

    Without multithreading, the server would have to close its current established
    TCP connection in order to establish a new connection with a new client to
    listen to its incoming messages. Multithreading allows for multiple TCP
    connections (one per client) to be open concurrently.

"""
from socket import *
import threading


class Server:
    """
    Server accepts TCP connections from 2 clients, X and Y. Once two connections are
    established, it receives messages from both clients. It formats the messages based
    on order of receipt and sends them back to the client.
    """

    ordinal = {
        1: "first",
        2: "second"
    }  # Used for print formatting
    client_names = ["X", "Y"]  # Names of first and second connections
    total_clients = 2  # Number of expected clients

    def __init__(self):
        self.serverPort = 12000
        self.hostname = '127.0.0.1'

        self.connections = []  # Holds established connections
        self.rcvd_msgs = []  # Holds received messages from clients
        self.client_threads = []  # Used to cleanup client threads

        # Server listens for TCP connections
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
            msg = "From Server: Client {} connected.".format(self.client_names[index])
            client.send(msg.encode())

    def recv_msg(self, connection):
        """
        Receives messages sent to "connection". Formats and displays message to console.
        :param connection: connectionSocket object associated with a client
        """
        client_name_index = self.connections.index(connection)
        # Accepts and decodes messages in an infinite loop
        while True:
            msg = connection.recv(1024).decode()
            # Exits loop if empty string received (other side closed connection)
            if not msg:
                break
            # Else stores and then prints confirmation of receipt of client message
            else:
                # Each client's message is stored in the order it was received
                self.rcvd_msgs.append((client_name_index, msg))
                index = self.rcvd_msgs.index((client_name_index, msg))
                print("Client {0} sent message {1}: {2}".format(
                    self.client_names[client_name_index],
                    index + 1,
                    msg))

    def enable_client_communication(self):
        """
        Starts threads to receive messages for all established connections. Meant to be
        called after all clients are connected.
        """
        for client in self.connections:
            thread = threading.Thread(target=self.recv_msg, args=(client,))
            self.client_threads.append(thread)
            thread.start()

    def client_feedback(self):
        """
        Formats messages received from both clients, noting the order, content and names
        of the senders. Sends this message to all clients.
        """
        # Tuples containing client name and message are unpacked, in order of receipt
        first_client, first_message = self.rcvd_msgs[0]
        sec_client, sec_message = self.rcvd_msgs[1]

        # Message is formatted based on unpacked tuples
        msg = "From Server: {0}: {1} received before {2}: {3}".format(
            self.client_names[first_client],
            first_message,
            self.client_names[sec_client],
            sec_message)

        # Message is sent to all clients
        for client in self.connections:
            client.send(msg.encode())

    def end_connections(self):
        """
        Ends connections with both clients and joins recv_msg threads.
        """
        for client in self.connections:
            self.client_threads[self.connections.index(client)].join()
            client.close()

    def run(self):
        """
        Main function for server.py.
        """

        # Server waits for both clients to connect and then sends confirmation messages
        print('The server is waiting to receive two connections....\n')
        self.conn_handler()
        self.confirmation_msg(self.connections)

        # Server begins to receive messages from clients.
        print("\nWaiting to receive messages from client X and client Y....\n")
        self.enable_client_communication()

        # Server waits until message from both clients is received
        while len(self.rcvd_msgs) < 2:
            pass

        # Server notifies clients of order/content of received messages
        self.client_feedback()
        print("\nWaiting a bit for clients to close their connections")

        # Server ends connections with clients and joins threads
        self.end_connections()

        print("Done.")


if __name__ == "__main__":
    tcp_serv = Server()
    tcp_serv.run()
