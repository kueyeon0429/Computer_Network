stream = input("bit stream > ")

result = []

if stream[0] == "0":
    cur_level = "0"
    result.append(cur_level)
    last_nonzero_level = "-"
else:
    cur_level = "+"
    result.append(cur_level)
    last_nonzero_level = "+"

for i in range(1, len(stream)):
    if stream[i] == "0":
        result.append(cur_level)
    else:
        if cur_level != "0":
            cur_level = "0"
            result.append(cur_level)
        else:
            if last_nonzero_level == "+":
                cur_level = "-"
                last_nonzero_level = "-"
                result.append(cur_level)
            elif last_nonzero_level == "-":
                cur_level = "+"
                last_nonzero_level = "+"
                result.append(cur_level)

print(''.join(result))