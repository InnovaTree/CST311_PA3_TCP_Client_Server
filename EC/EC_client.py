"""

"""

from socket import *
import threading


class Client:
    end_phrase = "Bye"

    def __init__(self):

        self.serverName = '127.0.0.1'
        self.serverPort = 12000
        self.end_chat = False

        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.clientSocket.connect((self.serverName, self.serverPort))

    def recv_msg(self):
        while not self.end_chat:
            msg = self.clientSocket.recv(1024).decode()
            if msg == self.end_phrase:
                self.end_chat = True
            elif msg:
                print(msg)

    def send_msg(self):
        while True:
            msg = input("")
            if not self.end_chat:
                self.clientSocket.send(msg.encode())
            else:
                break

    def run(self):

        thread = threading.Thread(target=self.send_msg, daemon=True)
        thread.start()
        self.recv_msg()
        self.clientSocket.close()


if __name__ == "__main__":
    tcp_client = Client()
    tcp_client.run()
