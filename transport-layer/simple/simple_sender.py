import socket
from threading import*


server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "localhost"
port = 8000
server_sock.bind((host, port))

class client(Thread):
    def __init__(self, socket, address):
        Thread.__init__(self)
        self.sock = socket
        self.addr = address
        self.start()

    def run(self):
        while 1:
            r = input()
            client_sock.send(r.encode())

server_sock.listen(5)
print("Sender ready and is listening")
while 1:
    client_sock, address = server_sock.accept()
    print("Receiver "+str(address)+" connected")
    client(client_sock, address)