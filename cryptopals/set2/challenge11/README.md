# **[set 2 - challenge 11](https://cryptopals.com/sets/2/challenges/11): An ECB/CBC detection oracle**

Now that you have ECB and CBC working:

Write a function to generate a random AES key; that's just 16 random bytes.

Write a function that encrypts data under an unknown key --- that is, a function that generates a random key and encrypts under it.

The function should look like:

```text
encryption_oracle(your-input)
=> [MEANINGLESS JIBBER JABBER]
```

Under the hood, have the function append 5-10 bytes (count chosen randomly) before the plaintext and 5-10 bytes after the plaintext.

Now, have the function choose to encrypt under ECB 1/2 the time, and under CBC the other half (just use random IVs each time for CBC). Use rand(2) to decide which to use.

Detect the block cipher mode the function is using each time. You should end up with a piece of code that, pointed at a block box that might be encrypting ECB or CBC, tells you which one is happening.

## What is oracle?

oracle means we can manually choose the input for the detection function.

But in order to detect ECB mode like challenge 8, there must be duplicate blocks in the ciphertext. => We need to find a plaintext so that there is a duplicate block in the ciphertext. Simple calculation:

- 2 block (16 bytes each block) are 32 bytes long
  - => Plaintext must have at least 32 consecutive identical characters
- But because of this function:

```text
Under the hood, have the function append 5-10 bytes (count chosen randomly) before the plaintext and 5-10 bytes after the plaintext.
```

- => Plaintext must have at least (32 + 10) = 42 consecutive identical characters to output 2 identical blocks after encrypt.

=> So the plaintext is: "a"*42

## Python code

python code:

- pkcs7, this function is a better version than [challenge 9 version](../challenge9/challenge9.py):

    ```python
    def pkcs7(message: bytes, blocksize: int) -> bytes:
        diff = blocksize - len(message) % blocksize

        padding = bytes([diff]*diff)

        ret = message + padding

        return ret
    ```

- append_5_10:

    ```python
    def append_5_10(plaintext: bytes):
        first = randint(5, 10)
        last = randint(5, 10)
        ret = urandom(first) + plaintext + urandom(last)

        return ret
    ```

- AES_encrypt with random mode (ECB/CBC):

    ```python
    # AES_encrypt with 50% chance ecb mode and 50% chance cbc mode
    def AES_encrypt(plaintext: bytes):
        keysize = 16
        blocksize = 16

        plaintext = append_5_10(plaintext)
        plaintext = pkcs7(plaintext, blocksize)

        r = randint(0, 1)
        key = urandom(keysize)
        iv = urandom(blocksize)

        if r == 0: #ECB
            print("used mode: ecb")
            cryptor = AES.new(key, AES.MODE_ECB)
            ciphertext = cryptor.encrypt(plaintext)
        elif r == 1: #CBC
            print("used mode: cbc")
            cryptor = AES.new(key, AES.MODE_CBC, iv)
            ciphertext = cryptor.encrypt(plaintext)

        return ciphertext
    ```

- detect_ECB function:
  - an edited version of [detect_ECB function from challenge 8](../../set1/challenge8/challenge8.py)

    ```python
    def detect_ECB(ciphertext: bytes, blocksize: int = 16):
        dict_cipher = {}
        for i in range(0, len(ciphertext), blocksize):
            blockk = ciphertext[i:i+blocksize]
            if blockk in dict_cipher:
                dict_cipher[blockk] += 1
            else:
                dict_cipher[blockk] = 1

        # Print out which block appears more than once
        for blockk in dict_cipher:
            if dict_cipher[blockk] > 1:
                print(f"block: {blockk}\ntimes: {dict_cipher[blockk]}")
                return True
        return False
    ```

source code: [here](./challenge11.py)

result:

```text
used mode: ecb
ciphertext: b'`\xdf\x8a\x99\xd1\xbe*\xe3/\x92\x9f\xf1\xd7/n\xb4@\xe0\x04wW$\xe3 !\xc3IX\xcc\x11=\xd3@\xe0\x04wW$\xe3 !\xc3IX\xcc\x11=\xd3Pq\xbe\x85\xaa\xf4\xc4\x93\x94uM\x08?Tu\xc5'
block: b'@\xe0\x04wW$\xe3 !\xc3IX\xcc\x11=\xd3'
times: 2
detected mode: ecb
```

```text
used mode: cbc
ciphertext: b"U'+\xf9\x8b6\xa6\x02\xc60\xea\x8b\xac9J\xecF\x93\xf7$\xee\xf8\xdf\xdd\x8c.\x07\xcfK\x8a5\x10\x82s_\xe9\xe4\x0e\xa6\xa7P'\x96\xf3\xf6\xf3\xeaw\x9b\xe9\xcd\xf8\xc2\xf4\x8b\r\x18cG\x8d\xbeK0\x15"
detected mode: cbc
```

## References
