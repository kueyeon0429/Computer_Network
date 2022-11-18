stream = input("bit stream > ")

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

print(''.join(result))