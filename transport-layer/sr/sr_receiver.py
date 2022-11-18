import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "localhost"
port = 8000
s.connect((host, port))

def try_ack(previous, current):
    if previous == current:
        return True
    else:
        return False

output = ""
ackNo = '0'

while 1:
    data = s.recv(1024).decode()
    print("Received --> " + data[1])
    if(data[1] == '-'):
        s.close()
        break
    if try_ack(ackNo, data[0]):
        ackNo = str((int(data[0])+1)%8)
        output = output + data[1]

    sendmsg = "ACK " + ackNo
    s.send(sendmsg.encode())


    print("the received bitstring is", output)