import socket
from multiprocessing import Process, Queue
import time
import random


# Application layer
def inputBitstring(bitstring, q):
    bitstr = bitstring.replace(" ", "")
    q.put(bitstr)
    print("Application layer> Delivering data to Transport layer ",bitstr)


# Transport layer
def stopwait(q):
    data = q.get()
    print("Transport layer> Receiving data from Application layer ",data)
    seqNo = str(0)
    print("Add seqNo 0 as header")
    packet = seqNo + data
    q.put(packet)
    print("Transport layer> Delivering data to Network layer ",packet)

def ack_stopwait(aq):
    ackmsg = aq.get()
    ack = ackmsg[:8] + " " + ackmsg[8:16] + " " + ackmsg[16:]
    print("Transport layer> Receiving ACK message from Datalink layer", ack)
    print("ACK message received complete ٩(ˊᗜˋ )و")


# Network layer
def bypass(q):
    data = q.get()
    q.put(data)
    print("Network layer> Receiving data from Transport layer ",data)
    print("Network layer> Delivering data to Datalink layer ",data)

def ack_bypass(aq):
    ack = aq.get()
    aq.put(ack)
    print("Network layer> Receiving ACK message from Transport layer ",ack)
    print("Network layer> Delivering ACK message to Datalink layer ",ack)


# Datalink layer
def csma_cd():
    success = False
    K_MAX = 15
    K = 0

    while (1):
        print("---------CSMA---------")
        while (1):
            busyOrIdle = random.randrange(1, 3)
            if busyOrIdle == 1:  # idle
                print("idle")
                break;
            else:
                print("busy")

        print("----------CD----------")
        collisionOrNot = random.randrange(1, 3)
        if collisionOrNot == 1:  # not -> success
            print("not collision -> success")
            success = True
            return success
        else:  # collision
            print("collision")
            print("send a jamming signal")
            print("-------Back_Off-------")
            K = K + 1
            print("K:", K)

        if K > K_MAX:  # abort
            print("abort")
            break;
        else:
            R = random.randrange(0, 2 ** K)

        # wait Tb time
        time.sleep(R * 0.001)
        print("wait~", R)

def bit_stuffing(q):
    data = q.get()
    print("Datalink layer> Receiving data from Network layer ",data)
    result = []
    bitstr = data

    count = 0
    for i in range(0, len(bitstr)):
        if bitstr[i] == "1":
            result.append("1")
            count = count + 1
        else:
            result.append("0")
            count = 0
        if count == 5:
            result.append("0")
            count = 0

    bitstr = ''.join(result)
    if(csma_cd() == True):
        q.put(bitstr)
        print("Datalink layer> Message bit-stuffing and Delivering data to Physical layer ",bitstr)

def bit_unstuffing(aq):
    ackmsg = aq.get()
    print("Datalink layer> Receiving ACK message from Physical layer ", ackmsg)
    result = []

    count = 0
    for i in range(0, len(ackmsg)):
        if ackmsg[i] == "1":
            result.append("1")
            count = count + 1
        else:
            if count != 5:
                result.append("0")
            count = 0

    ack = ''.join(result)
    aq.put(ack)
    print("Datalink layer> Message bit-unstuffing and Delivering ACK message to Network layer ", ack)


# Physical layer
def mlt_3(q):
    bitstr = q.get()
    bit_stuffed = []
    mlt_3 = []

    print("Physical layer> Receiving data from Datalink layer ",bitstr)

    count = 0
    for i in range(0, len(bitstr)):
        if bitstr[i] == "1":
            bit_stuffed.append("1")
            count = count + 1
        else:
            bit_stuffed.append("0")
            count = 0
        if count == 5:
            bit_stuffed.append("0")
            count = 0

    if bit_stuffed[0] == "0":
        cur_level = "0"
        mlt_3.append(cur_level)
        last_nonzero_level = "-"
    else:
        cur_level = "+"
        mlt_3.append(cur_level)
        last_nonzero_level = "+"

    for i in range(1, len(bit_stuffed)):
        if bit_stuffed[i] == "0":
            mlt_3.append(cur_level)
        else:
            if cur_level != "0":
                cur_level = "0"
                mlt_3.append(cur_level)
            else:
                if last_nonzero_level == "+":
                    cur_level = "-"
                    last_nonzero_level = "-"
                    mlt_3.append(cur_level)
                elif last_nonzero_level == "-":
                    cur_level = "+"
                    last_nonzero_level = "+"
                    mlt_3.append(cur_level)

    bitstr = ''.join(mlt_3)
    q.put(bitstr)
    client_sock.send(bitstr.encode())

    print("Physical layer> MLT-3 scheme and Sending data to receiver ",bitstr)

    ack = client_sock.recv(1024).decode()
    aq.put(ack)


def reverse_mlt_3(aq):
    ackmsg = aq.get()
    print("Physical layer> Receiving ACK message from sender ", ackmsg)
    un_mlt_3 = []
    bit_unstuffed = []

    if ackmsg[0] == "0":
        un_mlt_3.append("0")
        cur_level = ackmsg[0]

    else:
        un_mlt_3.append("1")
        cur_level = ackmsg[0]

    for i in range(1, len(ackmsg)):
        if ackmsg[i] != cur_level:
            un_mlt_3.append("1")
            cur_level = ackmsg[i]
        else:
            un_mlt_3.append("0")

    count = 0

    for i in range(0, len(un_mlt_3)):
        if un_mlt_3[i] == "1":
            bit_unstuffed.append("1")
            count = count + 1
        else:
            if count != 5:
                bit_unstuffed.append("0")
            count = 0

    ack = ''.join(bit_unstuffed)
    aq.put(ack)
    print("Physical layer> Reverse MLT-3 scheme and Delivering ACk message to Datalink layer", ack)



if __name__ == "__main__":
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "localhost"
    port = 8000
    server_sock.bind((host, port))
    server_sock.listen(5)

    client_sock, address = server_sock.accept()
    print("Receiver " + str(address) + " connected")

    q = Queue()
    aq = Queue()

    bitstring = str(input("Enter 2byte bit string(ex. 11110000 11110000) "))

    app = Process(target=inputBitstring, args=(bitstring, q))
    tns = Process(target=stopwait, args=(q, ))
    nwk = Process(target=bypass, args=(q,))
    dl = Process(target=bit_stuffing, args=(q,))
    phy = Process(target=mlt_3, args=(q,))
    ack_phy = Process(target=reverse_mlt_3, args=(aq,))
    ack_dl = Process(target=bit_unstuffing, args=(aq,))
    ack_nwk = Process(target=ack_bypass, args=(aq,))
    ack_tns = Process(target=ack_stopwait, args=(aq,))

    app.start()
    time.sleep(0.1)
    tns.start()
    time.sleep(0.1)
    nwk.start()
    time.sleep(0.1)
    dl.start()
    time.sleep(0.1)
    phy.start()
    time.sleep(0.1)
    ack_phy.start()
    time.sleep(0.1)
    ack_dl.start()
    time.sleep(0.1)
    ack_nwk.start()
    time.sleep(0.1)
    ack_tns.start()

    q.close()
    q.join_thread()
    aq.close()
    aq.join_thread()

    app.join()
    tns.join()
    nwk.join()
    dl.join()
    phy.join()
    ack_phy.join()
    ack_dl.join()
    ack_nwk.join()
    ack_tns.join()
