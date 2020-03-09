from my_library import mThreading
from socket import *

class Server:
    def __init__(self, ip=gethostbyname_ex(gethostname())[2][-1], port=8080):
        self.ip = ip
        self.port = port
        self._server = socket(AF_INET, SOCK_STREAM)
        self._server.bind((self.ip, self.port))
        self._recorded = set()
        self.connected = set()
        self.buffers = set()
        self.run = False

    def start(self, listen=None):
        if listen is None:
            self._server.listen()
        else:
            self._server.listen(listen)
        self.run = True
        self.handle_clients()
        self.send_clients()

    @mThreading.thread
    def handle_clients(self):
        while self.run:
            con, addr = self._server.accept()

            self.connected.add(con)
            self.handle_client(con)

    @mThreading.thread
    def send_client(self, client, buffer):
        client.send(buffer)

    @mThreading.thread
    def buffer_send_logic(self, client_sent, buffer):
        for client in self.connected:
            if client != client_sent:
                self.send_client(client, buffer)

    @mThreading.thread
    def send_clients(self):
        while True:
            for client_sent, buffer in set(self.buffers):
                self.buffer_send_logic(client_sent, buffer)
                self.buffers.remove((client_sent, buffer))

    @mThreading.thread
    def handle_client(self, client):
        while True:
            try:
                self.buffers.add((client, client.recv(4096)))
            except:
                import traceback
                traceback.print_exc()


if __name__ == '__main__':
    server = Server()
    server.start()
