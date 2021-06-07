"""
Header

Threading:

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
            msg = "Client {} has connected.".format(self.client_names[index])
            client.send(msg.encode())

    def recv_msg(self, connection):
        """
        Receives messages sent to "connection". Ends connection if message contains
        end phrase. Otherwise, formats and displays message to console.
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
        msg = "{0}: {1} received before {2}: {3}".format(
            self.client_names[first_client],
            first_message,
            self.client_names[sec_client],
            sec_message)

        # Message is sent to all clients
        for client in self.connections:
            client.send(msg.encode())

    def end_connections(self):
        """
        Asks each client to end its connections and joins recv_msg threads.
        """
        for client in self.connections:
            self.client_threads[self.connections.index(client)].join()
            # client.close()

    def run(self):
        """
        Main function for server.py.
        """

        # Server waits for both clients to connect and then sends confirmation messages
        print('The server is waiting to receive two connections....')
        self.conn_handler()
        self.confirmation_msg(self.connections)

        # Server begins to receive messages from clients.
        print("Waiting to receive messages from client X and client Y....")
        self.enable_client_communication()

        # Server waits until message from both clients is received
        while len(self.rcvd_msgs) < 2:
            pass

        # Server notifies clients of order/content of received messages
        self.client_feedback()
        print("Waiting a bit for clients to close their connections")

        # Server asks clients to end connections and joins threads
        self.end_connections()

        print("Done.")


if __name__ == "__main__":
    tcp_serv = Server()
    tcp_serv.run()
