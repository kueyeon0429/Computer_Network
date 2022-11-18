import random
import time

K_MAX = 15
K = 0

while(1):
    print("---------CSMA---------")
    while (1):
        busyOrIdle = random.randrange(1, 3)
        if busyOrIdle == 1:   # idle
            print("idle")
            break;
        else:
            print("busy")

    print("----------CD----------")
    collisionOrNot = random.randrange(1, 3)
    if collisionOrNot == 1:   # not -> success
        print("not collision -> success")
        break;
    else:   # collision
        print("collision")
        print("send a jamming signal")
        print("-------Back_Off-------")
        K = K + 1
        print("K:", K)

    if K > K_MAX:   # abort
        print("abort")
        break;
    else:
        R = random.randrange(0, 2**K)

    # wait Tb time
    time.sleep(R * 0.001)
    print("wait~", R)


