from math import ceil, log

# Convert a decimal into any base (2 - 36)
def dec2anybase(input, base, width):
    res = str()
    while input > 0:
        rem = input % base
        if rem >= 0 and rem <= 9:
            res += chr(rem + ord("0"))
        else:
            res += chr(rem - 10 + ord("A"))
        input = int(input / base)

    return res[::-1].zfill(ceil(log(2**width - 1, base)))
