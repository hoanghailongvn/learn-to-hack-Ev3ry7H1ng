from binascii import unhexlify
from os import urandom
import hashlib
from random import randint
from time import sleep, time

def bxor(b1: bytes, b2: bytes) -> bytes: # use xor for bytes
    result = b""
    for b1, b2 in zip(b1, b2):
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

# Server side
consistent_but_unknown_key = urandom(randint(1, 20))

def insecure_compare(file: str, signature: str):
    expected = hmac_sha1(bytes(file, 'utf-8'), consistent_but_unknown_key)
    b_signature = unhexlify(signature)

    for a, b in zip(expected, b_signature):
        if a == b:
            sleep(5/1000)
            continue
        else:
            return "500"
    
    return "200"

def attack():
    found = b""

    # brute force each byte of signature
    for i in range(20):
        # brute force
        history = [0]*256
        for _ in range(10):
            for j in range(256):
                bruteforce_signature = found[:i] + bytes([j]) + b"\x00" * (20 - i - 1)

                start_time = time()
                insecure_compare("foo", bruteforce_signature.hex())
                exe_time = time() - start_time

                history[j] += exe_time

        max_time = max(history)
        max_index = history.index(max_time)
        found += bytes([max_index])
        
        print(found.hex())
            


if __name__ == "__main__":
    expected = hmac_sha1(bytes("foo", 'utf-8'), consistent_but_unknown_key)
    print(f"expected hash: {expected.hex()}")

    attack()