import socket
from multiprocessing import Process, Queue
import random
import time


'''receiving'''
# Application layer
def inputBitstring(q):
    bitstr = q.get()
    bitstring = bitstr[:8] + " " + bitstr[8:]
    q.put(bitstring)
    print("Application layer> Receiving data from Transport layer ",bitstring)
    print("Message received complete ٩(ˊᗜˋ )و")


# Transport layer
def stopwait(q, aq):
    data = q.get()
    print("Transport layer> Receiving data from Network layer ",data)
    print("Remove seqNo 0")
    bitstream = data[1:]
    q.put(bitstream)
    print("Transport layer> Delivering data to Application layer ",bitstream)

    ackmsg = "01000001 01000011 01001011"
    ack = ackmsg.replace(" ","")
    aq.put(ack)
    print("Transport layer> Delivering ACK message to Network layer ", ack)


# Network layer
def bypass(q):
    data = q.get()
    q.put(data)
    print("Network layer> Receiving data from Datalink layer ",data)
    print("Network layer> Delivering data to Transport layer ",data)

def ack_bypass(aq):
    ack = aq.get()
    aq.put(ack)
    print("Network layer> Receiving ACK message from Transport layer ",ack)
    print("Network layer> Delivering ACK message to Datalink layer ",ack)


# Datalink layer
def csma_cd():
    sucess = False
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
            sucess = True
            return sucess
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

def bit_unstuffing(q):
    stream = q.get()
    print("Datalink layer> Receiving data from Physical layer ", stream)
    result = []

    count = 0
    for i in range(0, len(stream)):
        if stream[i] == "1":
            result.append("1")
            count = count + 1
        else:
            if count != 5:
                result.append("0")
            count = 0

    bitstr = ''.join(result)
    q.put(bitstr)
    print("Datalink layer> Message bit-unstuffing and Delivering data to Network layer ", stream)

def bit_stuffing(aq):
    ackmsg = aq.get()
    print("Datalink layer> Receiving ACK message from Network layer ",ackmsg)
    result = []

    count = 0
    for i in range(0, len(ackmsg)):
        if ackmsg[i] == "1":
            result.append("1")
            count = count + 1
        else:
            result.append("0")
            count = 0
        if count == 5:
            result.append("0")
            count = 0

    ack = ''.join(result)
    if(csma_cd() == True):
        aq.put(ack)
        print("Datalink layer> ACK Message bit-stuffing and Delivering ACK message to Physical layer ",ack)



# Physical layer
def reverse_mlt_3(q):
    stream = q.get()
    print("Physical layer> Receiving data from sender ", stream)
    un_mlt_3 = []
    bit_unstuffed = []

    if stream[0] == "0":
        un_mlt_3.append("0")
        cur_level = stream[0]

    else:
        un_mlt_3.append("1")
        cur_level = stream[0]

    for i in range(1, len(stream)):
        if stream[i] != cur_level:
            un_mlt_3.append("1")
            cur_level = stream[i]
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

    bitstr = ''.join(bit_unstuffed)
    q.put(bitstr)
    print("Physical layer> Reverse MLT-3 scheme and Delivering to Datalink layer", bitstr)

def mlt_3(aq):
    ackmsg = aq.get()
    bit_stuffed = []
    mlt_3 = []

    print("Physical layer> Receiving ACK message from Datalink layer ",ackmsg)

    count = 0
    for i in range(0, len(ackmsg)):
        if ackmsg[i] == "1":
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

    ack = ''.join(mlt_3)
    aq.put(ack)
    s.send(ack.encode())

    print("Physical layer> MLT-3 scheme and Sending ACK message to receiver ",ack)



if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "localhost"
    port = 8000
    s.connect((host, port))

    q = Queue()
    aq = Queue()

    data = s.recv(1024).decode()
    q.put(data)

    app = Process(target=inputBitstring, args=(q,))
    tns = Process(target=stopwait, args=(q, aq))
    nwk = Process(target=bypass, args=(q,))
    dl = Process(target=bit_unstuffing, args=(q,))
    phy = Process(target=reverse_mlt_3, args=(q,))

    ack_nwk = Process(target=ack_bypass, args=(aq,))
    ack_dl = Process(target=bit_stuffing, args=(aq,))
    ack_phy = Process(target=mlt_3, args=(aq,))



    phy.start()
    time.sleep(0.1)
    dl.start()
    time.sleep(0.1)
    nwk.start()
    time.sleep(0.1)
    tns.start()
    time.sleep(0.1)
    ack_nwk.start()
    time.sleep(0.1)
    app.start()
    time.sleep(0.1)
    ack_dl.start()
    time.sleep(0.1)
    ack_phy.start()

    q.close()
    q.join_thread()
    aq.close()
    aq.join_thread()

    phy.join()
    dl.join()
    nwk.join()
    tns.join()
    ack_nwk.join()
    app.join()
    ack_dl.join()
    ack_phy.join()

    s.close()

'''
    A = "01000001"
    C = "01000011"
    K = "01001011"
'''