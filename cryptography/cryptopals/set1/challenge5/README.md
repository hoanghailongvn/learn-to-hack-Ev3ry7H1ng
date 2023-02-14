# **[set 1 - challenge 5](https://cryptopals.com/sets/1/challenges/5): Implement repeating-key XOR**

Here is the opening stanza of an important work of the English language:

```text
Burning 'em, if you ain't quick and nimble
I go crazy when I hear a cymbal
```

Encrypt it, under the key "ICE", using repeating-key XOR.

In repeating-key XOR, you'll sequentially apply each byte of the key; the first byte of plaintext will be XOR'd against I, the next C, the next E, then I again for the 4th byte, and so on.

It should come out to:

```text
0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272
a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f
```

Encrypt a bunch of stuff using your repeating-key XOR function. Encrypt your mail. Encrypt your password file. Your .sig file. Get a feel for it. I promise, we aren't wasting your time with this.

## Analysis

Instead of xor with a single character, now we xor each message block with a longer key.

## Solutions

```python
from binascii import unhexlify

def repeating_key_xor(msg: bytes, key: bytes):
    ciphertext = []

    for i, c in enumerate(msg):
        ciphertext.append(msg[i] ^ key[i % len(key)])
    
    return bytes(ciphertext)

if __name__ == "__main__":
    plaintext = b"Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
    key = b"ICE"
    expected_ciphertext = b'0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f'

    # check
    print(repeating_key_xor(plaintext, key) == unhexlify(expected_ciphertext))
```

Result:

```text
True
```

## References
