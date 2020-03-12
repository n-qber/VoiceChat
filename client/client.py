from socket import *
from my_library import mThreading
from recorder import Recorder, ClientPlayer


class Client:
    def __init__(self, server_ip, server_port):
        self.client = socket(AF_INET, SOCK_DGRAM)
        self.recorder = Recorder()
        self.server_ip = server_ip
        self.server_port = server_port
        self.people = {}
        self.server_address = (self.server_ip, self.server_port)

    def _start(self):
        self.client.bind(('', 0))

    @mThreading.thread
    def send_audio(self):
        for buffer in self.recorder.audio_buffer():
            print(buffer[:20])
            self.client.sendto(buffer, self.server_address)

    @mThreading.thread
    def to_ip(self, buffer):
        ip, audio = buffer.split(b"\r\n", 1)

        if ip not in self.people.items():
            self.people[ip] = ClientPlayer()

        self.people[ip].add(audio)

    @mThreading.thread
    def receive_audio(self):
        while True:
            buffer, address = self.client.recvfrom(2**16)
            self.to_ip(buffer)

    def run(self):
        self._start()
        self.send_audio()
        self.receive_audio()


if __name__ == '__main__':
    client = Client("192.168.15.21", 8080)
    client.run()