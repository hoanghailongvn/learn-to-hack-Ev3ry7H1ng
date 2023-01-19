# **[set 1 - challenge 8](https://cryptopals.com/sets/1/challenges/8): Detect AES in ECB mode**

In [this file](./8.txt) are a bunch of hex-encoded ciphertexts.

One of them has been encrypted with ECB.

Detect it.

Remember that the problem with ECB is that it is stateless and deterministic; the same 16 byte plaintext block will always produce the same 16 byte ciphertext.

## Solutions

```python
import binascii
from Crypto.Cipher import AES

if __name__ == "__main__":
    with open("8.txt", "r") as file:
        ciphertext = (file.read())
        file.close()

    # count the number of times each 16-bit block appears and save to dict
    dict_cipher = {}
    for i, line in enumerate(ciphertext.split('\n')):
        b_line = binascii.unhexlify(line)

        dict_cipher[i] = {}
        for j in range(0, len(b_line), 16):
            blockk = b_line[j:j+16]
            if blockk in dict_cipher[i]:
                dict_cipher[i][blockk] += 1
            else:
                dict_cipher[i][blockk] = 1

    # print out which block appears more than once
    for line in dict_cipher:
        for blockk in dict_cipher[line]:
            if dict_cipher[line][blockk] != 1:
                print(f"line: {line}")
                print(f"block: {blockk}\ntimes: {dict_cipher[line][blockk]}")
```

result:

```text
line: 132
block: b'\x08d\x9a\xf7\r\xc0oO\xd5\xd2\xd6\x9ctL\xd2\x83'
times: 4
```

in line 132, there is a block appearing 4 times => Most likely this line is encrypted with ECB

## References
