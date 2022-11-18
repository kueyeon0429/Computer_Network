stream = input("bit stream > ")

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

print(''.join(bit_unstuffed))