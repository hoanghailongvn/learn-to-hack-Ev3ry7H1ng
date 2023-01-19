# [BabyEncryption](https://app.hackthebox.com/challenges/babyencryption)

## CHALLENGE DESCRIPTION

You are after an organised crime group which is responsible for the illegal weapon market in your country. As a secret agent, you have infiltrated the group enough to be included in meetings with clients. During the last negotiation, you found one of the confidential messages for the customer. It contains crucial information about the delivery. Do you think you can decrypt it?

## Files

[here](./BabyEncryption/)

## Analysis

the encryption function is pretty simple:

```python
def encryption(msg):
    ct = []
    for char in msg:
        ct.append((123 * char + 18) % 256)
    return bytes(ct)
```

When I first looked at it I wondered if there was a case where two different inputs produced the same output. But if that's the case, it can't be decrypted. So let's build a simple decrypt function.

## Decrypt

[source](./decrypt.py)

```python
import string
from binascii import hexlify, unhexlify

def encryption(msg):
    ct = []
    for char in msg:
        ct.append((123 * ord(char) + 18) % 256)
    return bytes(ct)

maps = {}
# build a reverse dictionary
for char in string.printable:
    maps[encryption(char)] = char

# decrypt each character
with open('./BabyEncryption/msg.enc','r') as file:
    ciphertext = unhexlify(file.read())
    plaintext = ""
    for c in ciphertext:
        plaintext += maps[c.to_bytes(1, 'little')]
    print(plaintext)
```

result:

```text
Th3 nucl34r w1ll 4rr1v3 0n fr1d4y.
HTB{l00k_47_y0u_r3v3rs1ng_3qu4710n5_c0ngr475}
```
