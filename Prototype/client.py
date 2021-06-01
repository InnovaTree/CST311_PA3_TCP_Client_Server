"""

"""

from socket import *
import threading


class Client:
    end_phrase = "Bye"

    def __init__(self):
        self.serverName = '127.0.0.1'
        self.serverPort = 12000
        self.msg_recvd = False

        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.clientSocket.connect((self.serverName, self.serverPort))

    def recv_msg(self):
        while True:
            msg = self.clientSocket.recv(1024).decode()
            if msg == self.end_phrase:
                self.clientSocket.send(self.end_phrase.encode())
                self.clientSocket.close()
                break
            elif msg:
                print(msg)
                self.msg_recvd = True

    def run(self):
        thread = threading.Thread(target=self.recv_msg)
        thread.start()

        while not self.msg_recvd:
            pass

        sentence = input('Enter message to send to server: ')
        self.clientSocket.send(sentence.encode())

        thread.join()


if __name__ == "__main__":
    tcp_client = Client()
    tcp_client.run()