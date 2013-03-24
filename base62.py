#!/usr/bin/env python

#def f(start, end):
#	return [chr(i) for i in range(ord(start), ord(end) + 1)]
#
#keys = f('a', 'z') + f('A', 'Z') + f('0', '9')
#
#random.shuffle(keys)
#print keys
#
#ALPHABET = ''.join(keys)
#print ALPHABET

ALPHABET = "nyU9j2W7Hv3MNTtZb1qhwG6O84PKFpdRJVSsDAalLfIrgziXBCkoxQmucYEe05"

def base62_encode(num, alphabet=ALPHABET):
    """Encode a number in Base X

    `num`: The number to encode
    `alphabet`: The alphabet to use for encoding
    """
    if (num == 0):
        return alphabet[0] * 5
    arr = []
    base = len(alphabet)
    while num:
        rem = num % base
        num = num // base
        arr.append(alphabet[rem])
    arr.reverse()
    return ''.join(arr).rjust(5,alphabet[0])

def base62_decode(string, alphabet=ALPHABET):
    """Decode a Base X encoded string into the number

    Arguments:
    - `string`: The encoded string
    - `alphabet`: The alphabet to use for encoding
    """
    base = len(alphabet)
    strlen = len(string)
    num = 0

    idx = 0
    for char in string:
        power = (strlen - (idx + 1))
        num += alphabet.index(char) * (base ** power)
        idx += 1

    return num
