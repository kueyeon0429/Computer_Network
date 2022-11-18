# Computer Network

## Run
1. open two terminals  
2. execute each of the commands below  
    **[sender]**  
    ```
    python3 sender.py
    ```
    **[receiver]**
    ```
    python3 receiver.py
    ```
3. enter 2byte bitstream as the input of the sender. (ex. 11110000 11110000)


## Sender
### Application layer
**def inputBitstring(bitstring, q)** : 입력받은 스트링 저장
1. main 함수에서 입력받은 bitstring에서 공백을 제거
2. q(Queue)에 put
### Transport layer
**def stopwait(q)**: (sender->receive) stop and wait, 시퀀스 넘버 추가
1. q(Queue)에서 데이터를 get
2. 데이터 앞에 시퀀스넘버(seqNo)를 붙인 packet 생성  

**def ack_stopwait(aq)**: (receive->sender) stop and wait, ack메세지 수신
1. aq(Queue)에서 ack데이터를 get
2. ack데이터에 1byte단위로 공백 추가
3. ACK 메세지 수신 완료 메세지
### Network layer
**def bypass(q)**: (sender->receive)  
**def ack_bypass(aq)**: (receive->sender)
1. bypass
### Datalink layer
**def csma_cd()**: (receive->sender) csma/cd, bit_stuffing 함수 내에서 호출
1. not collision -> success 이면 success = True를 리턴  

**def bit_stuffing(q)**: (sender->receive) bit_stuffing
1. q(Queue)에서 데이터 get
2. result 리스트 생성
3. result 리스트에 bit_stuffing한 데이터 저장
4. result 리스트 요소들을 string으로 bitstr에 저장
5. q에 bitstr을 put  

**def bit_unstuffing(aq)**: (receive->sender) bit_unstuffing
1. aq(Queue)에서 ack데이터를 get
2. result 리스트 생성
3. result 리스트에 unstuffing한 ack데이터 저장
4. result 리스트 요소들을 string으로 ack에 저장
5. aq에 ack put  
### Physical layer
**def mlt_3(q)**: (sender->receive) stop and wait, ack메세지 수신
1. q(Queue)에서 데이터 get
2. bit_stuffed 리스트, mlt_3 리스트 생성
3. mlt_3한 데이터 mlt_3리스트에 저장
4. mlt_3 리스트 요소들을 string으로 bitstr에 저장
5. q에 bitstr put
6. 클라이언트로부터 ack메세지 수신  

**def reverse_mlt_3(aq)**: (receive->sender) stop and wait, ack메세지 수신
1. aq(Queue)에서 ack 데이터 get
2. bit_unstuffed 리스트, un_mlt_3 리스트 생성
3. un_mlt_3한 데이터 un_mlt_3리스트에 저장
4. un_mlt_3 리스트 요소들을 string으로 ack에 저장
5. aq에 ack put
### main
1. 소켓 생성 및 바인딩
2. a(sender->receiver), aq(receiver->sender) 큐 생성
3. bitstream 입력
4. 각종 프로세스 생성

## Receiver
### Application layer
**def inputBitstring(bitstring, q)** : receive message
1. q(Queue)에서 데이터 get
2. 데이터에 byte 단위로 공백 추가
3. q에 put
4. 메세지 수신 완료.
### Transport layer
**def stopwait(q, aq)**: (sender<->receive) stop and wait, ack메세지 생성
1. q에서 데이터 get
2. 시퀀스 넘버 제거
3. q에 put
4. ack메세지 생성
5. ack 메세지 공백 제거
6. aq에 put
### Network layer
**def bypass(q)**: (sender->receive)  
**def ack_bypass(aq)**: (receive->sender)
1. bypass
### Datalink layer
**def csma_cd()**: (receive->sender) csma/cd, bit_stuffing 함수 내에서 호출
1. not collision -> success 이면 success = True를 리턴
def bit_unstuffing(q): (sender->receive) bit_stuffing
1. q(Queue)에서 데이터 get
2. result 리스트 생성
3. result 리스트에 unstuffing한 데이터 저장
4. result 리스트 요소들을 string으로 bitstr에 저장  
5. q에 bitstr을 put  

**def bit_stuffing(aq)**: (receive->sender) bit_unstuffing
1. aq(Queue)에서 ack데이터를 get
2. result 리스트 생성
3. result 리스트에 stuffing한 ack데이터 저장
4. result 리스트 요소들을 string으로 ack에 저장
5. aq에 ack put
### Physical layer
**def reverse_mlt_3(q)**: (sender->receive) stop and wait, ack메세지 수신
1. q(Queue)에서 데이터 get
2. bit_unstuffed 리스트, un_mlt_3 리스트 생성
3. un_mlt_3한 데이터 un_mlt_3리스트에 저장
4. un_mlt_3 리스트 요소들을 string으로 bitstr에 저장
5. q에 bitstr put
6. sender로부터 메세지 수신  

**def mlt_3(aq)**: (receive->sender) stop and wait, ack메세지 수신
1. aq(Queue)에서 ack 데이터 get
2. bit_stuffed 리스트, mlt_3 리스트 생성
3. mlt_3한 데이터 mlt_3리스트에 저장
4. mlt_3 리스트 요소들을 string으로 ack에 저장
5. aq에 ack put
### main
1. 소켓 생성 및 바인딩
2. a(sender->receiver), aq(receiver->sender) 큐 생성
3. bitstream 입력
4. 각종 프로세스 생성
5. 소켓 close