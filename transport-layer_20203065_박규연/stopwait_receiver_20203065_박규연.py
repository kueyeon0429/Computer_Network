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

while 2:
    data = s.recv(1024).decode()
    print("Received --> " + data[1])
    if try_ack(ackNo, data[0]):
        ackNo = str((int(data[0])+1)%2)
        output = output + data[1]

    sendmsg = "ACK " + ackNo
    s.send(sendmsg.encode())


    print("the received bitstring is", output)

s.close()