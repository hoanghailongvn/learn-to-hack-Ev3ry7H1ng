import string
from binascii import hexlify, unhexlify

maps = {}

def encryption(msg):
    ct = []
    for char in msg:
        ct.append((123 * ord(char) + 18) % 256)
    return bytes(ct)

for char in string.printable:
    maps[encryption(char)] = char

with open('./BabyEncryption/msg.enc','r') as file:
    ciphertext = unhexlify(file.read())
    plaintext = ""
    for c in ciphertext:
        plaintext += maps[c.to_bytes(1, 'little')]
    print(plaintext)




