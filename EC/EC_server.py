from socket import *
import threading


class ECServer:
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
        self.client_threads = []
        self.end_chat = False

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
            msg = "[Server] Client {} has connected.".format(self.client_names[index])
            client.send(msg.encode())

    def recv_msg(self, connection):
        client_name = self.connections.index(connection)
        while not self.end_chat:
            msg = connection.recv(1024).decode()
            if msg:
                self.broadcast(msg, self.client_names[client_name])
                if msg == self.end_phrase:
                    self.end_chat = True

    def broadcast(self, msg, name="[Server]"):
        modified_msg = "{0}: {1}".format(name, msg)
        print(modified_msg)
        for client in self.connections:
            client.send(modified_msg.encode())

    def enable_client_communication(self):
        for client in self.connections:
            thread = threading.Thread(target=self.recv_msg, args=(client,))
            self.client_threads.append(thread)
            thread.start()

    def end_connections(self):
        for client in self.connections:
            client.send("[Server] Ended your connection.".encode())
            client.send(self.end_phrase.encode())

        for thread in self.client_threads:
            thread.join()

        for client in self.connections:
            client.close()

    def run(self):
        print('The server is waiting to receive two connections....')
        self.conn_handler()
        self.confirmation_msg(self.connections)

        print("Waiting to receive messages from client X and client Y....")
        self.enable_client_communication()

        while not self.end_chat:
            pass

        print("Waiting a bit for clients to close their connections")
        self.end_connections()
        print("Done.")


if __name__ == "__main__":
    tcp_serv = ECServer()
    tcp_serv.run()
