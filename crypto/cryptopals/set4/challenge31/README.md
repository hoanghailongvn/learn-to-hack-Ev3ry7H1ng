# **[set 4 - challenge 31](https://cryptopals.com/sets/4/challenges/31): Implement and break HMAC-SHA1 with an artificial timing leak**

The psuedocode on Wikipedia should be enough. HMAC is very easy.

Using the web framework of your choosing (Sinatra, web.py, whatever), write a tiny application that has a URL that takes a "file" argument and a "signature" argument, like so:

```url
http://localhost:9000/test?file=foo&signature=46b4ec586117154dacd49d664e5d63fdc88efb51
```

Have the server generate an HMAC key, and then verify that the "signature" on incoming requests is valid for "file", using the "==" operator to compare the valid MAC for a file with the "signature" parameter (in other words, verify the HMAC the way any normal programmer would verify it).

Write a function, call it "insecure_compare", that implements the == operation by doing byte-at-a-time comparisons with early exit (ie, return false at the first non-matching byte).

In the loop for "insecure_compare", add a 50ms sleep (sleep 50ms after each byte).

Use your "insecure_compare" function to verify the HMACs on incoming requests, and test that the whole contraption works. Return a 500 if the MAC is invalid, and a 200 if it's OK.

Using the timing leak in this application, write a program that discovers the valid MAC for any file.

Why artificial delays?

```text
Early-exit string compares are probably the most common source of cryptographic timing leaks, but they aren't especially easy to exploit. In fact, many timing leaks (for instance, any in C, C++, Ruby, or Python) probably aren't exploitable over a wide-area network at all. To play with attacking real-world timing leaks, you have to start writing low-level timing code. We're keeping things cryptographic in these challenges.
```

## HMAC

HMAC is a special type of MAC that protects against length extension attacks as exploited in challenge 29 + 30.

Pseudocode [here](https://en.wikipedia.org/wiki/HMAC#Implementation)

python code:

```python
import hashlib

def bxor(b1: bytes, b2: bytes) -> bytes: # use xor for bytes
    result = b""
    for b1, b2 in zip(b1, b2):
        print(b1, b2)
        result += bytes([b1 ^ b2])
    return result

def sha1(message: bytes) -> bytes:
    h = hashlib.sha1()
    h.update(message)
    return h.digest()

def hmac_sha1(message: bytes, key: bytes) -> bytes:
    ipad = b'\x36' * 64
    opad = b'\x5C' * 64

    if len(key) > 64:
        key = sha1(key)

    if len(key) < 64:
        key = key.ljust(64, b"\x00")

    return sha1(bxor(key, opad) + sha1(bxor(key, ipad) + message))
```

## Timing attack

[Wikipedia](https://en.wikipedia.org/wiki/Timing_attack): Every logical operation in a computer takes time to execute, and the time can differ based on the input; with precise measurements of the time for each operation, an attacker can work backwards to the input.

in the challenge 31 + 32, insecure_compare() functiontakes 2 strings, compares each byte from left to right, time to compare is quite substantialsuy (50ms each byte). depends on server response time delay, attacker can use bruteforce technique to find the secret

## implement server-side code

insecure_compare():

```python
# Server side
def random_bytes(length: int) -> bytes:
    ret = []
    for _ in range(length):
        ret.append(randint(0, 255))
    
    return bytes(ret)

consistent_but_unknown_key = random_bytes(randint(1, 20))

def insecure_compare(file: str, signature: str):
    expected = hmac_sha1(bytes(file, 'utf-8'), consistent_but_unknown_key)
    print(f"expected hash: {expected.hex()}")

    b_signature = unhexlify(signature)

    for a, b in zip(expected, b_signature):
        if a == b:
            sleep(50/1000)
            continue
        else:
            return "500"
    
    return "200"
```

## Attack

bruteforce:

```python
def attack():
    found = b""

    # brute force each byte of signature
    for i in range(20):
        max_time = -inf

        # brute force
        for j in range(256):
            bruteforce_signature = found[:i] + bytes([j]) + b"\x00" * (20 - i - 1)

            start_time = time()
            insecure_compare("foo", bruteforce_signature.hex())
            exe_time = time() - start_time

            if exe_time > max_time:
                found = found[:i] + bytes([j])
                max_time = exe_time
        
        print(found.hex())
```

result:

```text
expected hash: 50a90948db290cc9c63991e4ffc562cfeaf98624
50
50a9
50a909
50a90948
50a90948db
50a90948db29
Traceback (most recent call last):
  File "f:\Desktop\innerDesktop\week10\set4\challenge31\challenge31.py", line 80, in <module>
    attack()
  File "f:\Desktop\innerDesktop\week10\set4\challenge31\challenge31.py", line 65, in attack
    insecure_compare("foo", bruteforce_signature.hex())
  File "f:\Desktop\innerDesktop\week10\set4\challenge31\challenge31.py", line 46, in insecure_compare
    sleep(50/1000)
KeyboardInterrupt
```

I interrupt the program because we can see it is working fine, and to get the result, we need: 20 \* 256 \* 20 \* 50 = 5120000 (ms) = 1.42222222 (hours):

- 20: bruteforce positions
- 256: 1 bytes = 256 case
- 20: worst case 20 bytes
- 50: server compare time

## References

Timing attack: <https://en.wikipedia.org/wiki/Timing_attack>
