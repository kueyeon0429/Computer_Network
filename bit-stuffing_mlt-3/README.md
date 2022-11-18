# Bit-Stuffing and MLT-3 Interworking with sender and receiver
Data-linkn layer의 bit-stuffing 결과를 Pysical layer의 MLT-3 알고리즘의 입력값으로 넣어 결과를 출력

## Sender
- input
- Data-link layer: bit-stuffing
- Pysical layer: MLT-3

## Receiver
- Pysical layer: MLT-3
- Data-link layer: bit-stuffing
- output

### Example
```
o input
    11111111

o Data-link layer
    bit-stuffing -> 111110111

o Physical layer
    MLT-3 -> +0-0++0-0
```

```
o input
    +0-0++0-0

o Physical layer
    MLT-3 -> 111110111

o Data-link layer
    bit-unstuffing -> 11111111
```
