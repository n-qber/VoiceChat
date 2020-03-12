from socket import *
from my_library import mThreading

@mThreading.thread
def send_things_to_server(name):
    s = socket(AF_INET, SOCK_STREAM)
    s.connect(("192.168.15.21", 8080))
    s.send(b"HEY, MY NAME IS " + name.encode())
    while True:
        print(name, s.recv(4096))


if __name__ == '__main__':
    send_things_to_server("josh")
    send_things_to_server("lucas")
    send_things_to_server("nociasd")
