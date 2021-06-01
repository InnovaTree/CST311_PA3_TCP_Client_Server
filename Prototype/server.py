from socket import *
import threading


class Server:
    ordinal = {
        1: "first",
        2: "second"
    }
    client_names = ["X", "Y"]
    total_clients = 2
    end_phrase = "Bye"

    def __init__(self):
        self.serverPort = 12000
        self.hostname = '127.0.0.1'

        self.connections = []
        self.rcvd_msgs = []
        self.client_threads = []

        self.serverSocket = socket(AF_INET, SOCK_STREAM)
        self.serverSocket.bind((self.hostname, self.serverPort))
        self.serverSocket.listen(1)

    def conn_handler(self):
        while len(self.connections) < self.total_clients:
            connectionSocket, addr = self.serverSocket.accept()
            self.connections.append(connectionSocket)

            index = self.connections.index(connectionSocket)
            print("Accepted {0} connection, calling it client {1}".format(
                self.ordinal[index + 1],
                self.client_names[index]))

    def confirmation_msg(self, conn_list):
        for client in conn_list:
            index = conn_list.index(client)
            msg = "Client {} has connected.".format(self.client_names[index])
            client.send(msg.encode())

    def recieve(self, connection):
        client_name = self.connections.index(connection)
        while True:
            msg = connection.recv(1024).decode()
            if msg == self.end_phrase:
                connection.close()
                break
            elif msg:
                self.rcvd_msgs.append((client_name, msg))
                index = self.rcvd_msgs.index((client_name, msg))
                print("Client {0} sent message {1}: {2}".format(
                    self.client_names[index],
                    index + 1,
                    msg))

    def enable_client_communication(self):
        for client in self.connections:
            thread = threading.Thread(target=self.recieve, args=(client,))
            self.client_threads.append(thread)
            thread.start()

    def client_feedback(self):
        first_client, first_message = self.rcvd_msgs[0]
        sec_client, sec_message = self.rcvd_msgs[1]
        msg = "{0}: {1} received before {2}: {3}".format(
            self.client_names[first_client],
            first_message,
            self.client_names[sec_client],
            sec_message)
        for client in self.connections:
            client.send(msg.encode())

    def end_connections(self):
        for client in self.connections:
            client.send(self.end_phrase.encode())

        for thread in self.client_threads:
            thread.join()

    def run(self):
        print('The server is waiting to receive two connections....')
        self.conn_handler()
        self.confirmation_msg(self.connections)

        print("Waiting to receive messages from client X and client Y....")
        self.enable_client_communication()
        while len(self.rcvd_msgs) < 2:
            pass

        self.client_feedback()
        print("Waiting a bit for clients to close their connections")
        self.end_connections()
        print("Done.")


if __name__ == "__main__":
    tcp_serv = Server()
    tcp_serv.run()
