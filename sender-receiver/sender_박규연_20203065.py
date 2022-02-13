stream = input("bit stream > ")

bit_stuffed = []
mlt_3 = []

count = 0
for i in range(0, len(stream)):
    if stream[i] == "1":
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

print(''.join(mlt_3))