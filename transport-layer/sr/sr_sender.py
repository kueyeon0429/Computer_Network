import socket
from threading import*
import threading
import time


server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "localhost"
port = 8000
server_sock.bind((host, port))


class client(Thread):

    size = 7
    Sf = []
    Sn = [0, 1, 2, 3, 4, 5, 6]
    global i
    global bitstring
    flag = threading.Event()

    def __init__(self, socket, address):
        Thread.__init__(self)
        self.sock = socket
        self.addr = address
        self.start()


    def timer(self, lock):
        lock.acquire()
        #if flag.wait(timeout=1):


    def sending(self):
        while self.i < len(self.bitstring):
            seqNo = self.Sn[0]
            packet = str(seqNo) + self.bitstring[self.i]
            client_sock.send(packet.encode())
            self.i += 1
            # timer start
            print("sending packet: seqNo_"+str(seqNo))
            self.Sf.append(packet)
            del self.Sn[0]
            time.sleep(1)
        seqNo = self.Sn[0]
        packet = str(seqNo)+'-'
        client_sock.send(packet.encode())
        client_sock.close()



    def receiving(self):
        while 1:
            client_sock.settimeout(1.001)
            try:
                ack = client_sock.recv(1024).decode()
                # timer stop
                if self.Sf[0][0] == str((int(ack[4])-1)%8):
                    print(ack)
                    del self.Sf[0]
                    self.Sn.append((self.Sn[-1]+1) % 8)
            except:
                try:
                    print("timeout! resend seqNo: "+ self.Sf[0][0])
                    continue
                except:
                    client_sock.close()
                    break


    def run(self):
        s = threading.Thread(target=self.receiving)
        r = threading.Thread(target=self.sending)
        self.bitstring = str(input("enter bit string "))
        self.i = 0
        s.start()
        r.start()
        s.join()
        r.join()



server_sock.listen(5)
print("Sender ready and is listening")
while 1:
    client_sock, address = server_sock.accept()
    print("Receiver "+str(address)+" connected")
    client(client_sock, address)