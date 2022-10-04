import socket

class Client:
    def __init__(self , connection , address):
        self.connection = connection
        self.address = address

    def send(self , data):
        self.connection.send(str(data).encode())

    def recv(self):
        byts = self.connection.recv(1024)
        return byts.decode()

    def get_ip(self):
        return self.address[0]

    def get_port(self):
        return self.address[1]

    def recvb(self):
        byts = self.connection.recv(1024)
        return byts