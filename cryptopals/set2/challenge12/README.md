# **[set 2 - challenge 12](https://cryptopals.com/sets/2/challenges/12): Byte-at-a-time ECB decryption (Simple)**

Copy your oracle function to a new function that encrypts buffers under ECB mode using a consistent but unknown key (for instance, assign a single random key, once, to a global variable).

Now take that same function and have it append to the plaintext, BEFORE ENCRYPTING, the following string:

```hexa
Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg
aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq
dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg
YnkK
```

Spoiler alert.

```text
Do not decode this string now. Don't do it.
```

Base64 decode the string before appending it. Do not base64 decode the string by hand; make your code do it. The point is that you don't know its contents.

What you have now is a function that produces:

```code
AES-128-ECB(your-string || unknown-string, random-key)
```

It turns out: you can decrypt "unknown-string" with repeated calls to the oracle function!

Here's roughly how:

1. Feed identical bytes of your-string to the function 1 at a time --- start with 1 byte ("A"), then "AA", then "AAA" and so on. Discover the block size of the cipher. You know it, but do this step anyway.
2. Detect that the function is using ECB. You already know, but do this step anyways.
3. Knowing the block size, craft an input block that is exactly 1 byte short (for instance, if the block size is 8 bytes, make "AAAAAAA"). Think about what the oracle function is going to put in that last byte position.
4. Make a dictionary of every possible last byte by feeding different strings to the oracle; for instance, "AAAAAAAA", "AAAAAAAB", "AAAAAAAC", remembering the first block of each invocation.
5. Match the output of the one-byte-short input to one of the entries in your dictionary. You've now discovered the first byte of unknown-string.
Repeat for the next byte.

## Analysis

can be considered as this challenge puts us in the case:

- let's say we are the client, and the other side is the server
- On the server side, there is an AES-128-ECB encryption function, it works by concatenating input with a secret unknown string, and encrypting that with a consistent, unchanged key.
- and on the client side, we can control what the input is and observe the ciphertext

Our mission is to exploit to get the secret unknown string appended after our input.

To do this, just follow the instructions.

## oracle function AES

- python code:

```python
import base64
from random import randint
from Crypto.Cipher import AES

def random_bytes(length: int) -> bytes:
    ret = []
    for _ in range(length):
        ret.append(randint(0, 255))
    
    return bytes(ret)

consistent_but_unknown_key = random_bytes(16)
unknown_target_bytes = base64.b64decode(b"""
Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg
aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq
dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg
YnkK
""")

def AES_encrypt_ECB_mode(attacker_controlled: bytes):
    blocksize = 16

    plaintext = attacker_controlled + unknown_target_bytes
    plaintext = pkcs7(plaintext, blocksize)

    cryptor = AES.new(consistent_but_unknown_key, AES.MODE_ECB)
    ciphertext = cryptor.encrypt(plaintext)

    return ciphertext
```

## Solution

follow the instructions:

- Step 1: Find blocksize
  - generate `attacker_controlled` with increasing length
  - observe the output, when some bytes at the beginning do not change after increasing the input length, it means that the length of the block does not change is the blocksize
  - python code:

    ```python
    def find_blocksize():
        prev_first_two_bytes = AES_encrypt_ECB_mode(b'a')[:2]

        # `attacker_controlled` with increasing length
        for i in range(2, 100):
            first_two_bytes = AES_encrypt_ECB_mode(bytes('a'*i, 'ascii'))[:2]
            # check if the first two bytes of ciphertext don't change after increasing attacker_controlled length
            if prev_first_two_bytes == first_two_bytes:
                return i - 1
            else:
                prev_first_two_bytes = first_two_bytes
    ```

  - result: blocksize = 16

- Step 2: check what block cipher mode is being used
  - with blocksize = 16, try entering input with 32 identical characters. Compare block 1 and block 2, if its equal, it means that ECB mode is being used.
  - python code:

    ```python
    def is_ecb(blocksize: int = 16):
        attacker_controlled = bytes('a'*32, 'ascii')
        ciphertext = AES_encrypt_ECB_mode(attacker_controlled)
        if ciphertext[0:blocksize] == ciphertext[blocksize:blocksize*2]:
            return True
        else:
            return False
    ```

  - result: True

- Step 3: find the first character of secret unknown string
  - craft an input `attacker_controlled` that the size is exactly 1 byte short, ex 'a'*15:
  - our input is concatenated with secret unknown string so the first character of `unknown secret string` will be filled in the missing byte
  - we have the `AES-128-ECB(attacker_controlled || first character of unknown-string, random-key)` ciphertext block. now we can try bruteforce to know what the first character is.
  - python code:

    ```python
    def crack():
        # b'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c'
        b_printable = string.printable

        ciphertext = AES_encrypt_ECB_mode(bytes('a'*15, 'ascii'))

        target_bytes = ''

        for c in b_printable:
            brute_force_ciphertext = AES_encrypt_ECB_mode(bytes('a'*15 + c, 'ascii'))
            if brute_force_ciphertext[:16] == ciphertext[:16]:
                target_bytes += c
                break
        
        print(target_bytes)
    ```

  - Result: the first character of `secret` is `R`:

- Step ...: Similarly, find the letter by letter of the `secret`
  - find the length of `secret` (padded): 144

    ```python
    ciphertext = AES_encrypt_ECB_mode(b'')
    print(len(ciphertext))
    ```

  - if we only use the input of length 1 blocksize, we can only extract 1 blocksize of characters of secret. so with a length of 144 of secret, our input must be the same size as secret, now we bruteforce at position 144
  - after finding the first character, we go find the second character:
    - `attacker_controlled`: 'a'*142
    - brute_force_attacker_controlled = attacker_controlled + `the first letter of the secret has been found` + {prinable character}
  - similarly we will get all the characters of `secret`

    ```python
    def crack():
        # b'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c'
        printable = string.printable

        len_target_bytes = 144
        target_bytes = ''

        for i in range(len_target_bytes):
            attacker_controlled = bytes('a'*(len_target_bytes - i - 1), 'ascii')
            ciphertext = AES_encrypt_ECB_mode(attacker_controlled)

            for c in printable:
                brute_force_attacker_controlled = attacker_controlled + bytes(target_bytes, 'ascii') + bytes(c, 'ascii')
                brute_force_ciphertext = AES_encrypt_ECB_mode(brute_force_attacker_controlled)
                if brute_force_ciphertext[128:144] == ciphertext[128:144]:
                    target_bytes += c
                    break
        return target_bytes
    ```

    Result:

    ```text
    Rollin' in my 5.0
    With my rag-top down so my hair can blow
    The girlies on standby waving just to say hi
    Did you stop? No, I just drove by

    ```

    Source code: [link](./challenge12.py)

## References
