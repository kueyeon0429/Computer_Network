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
            bitstring = str(input("enter bit string "))

            i = 0
            while i < len(bitstring):
                packet = str(i%2) + bitstring[i]
                client_sock.send(packet.encode())
                client_sock.settimeout(0.1)
                try:
                    ack = client_sock.recv(1024).decode()
                    print(ack)
                    i += 1
                except:
                    print("timeout! resend")
                    continue

server_sock.listen(5)
print("Sender ready and is listening")
while 1:
    client_sock, address = server_sock.accept()
    print("Receiver "+str(address)+" connected")
    client(client_sock, address)