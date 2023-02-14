from os import urandom
from random import randrange
from time import time
import struct
from MT19937 import MT19937_32

# xor 2 bytes object theo cái ngắn hơn
def stream_xor(input1: bytes, input2: bytes) -> bytes:
    shorter = min(len(input1), len(input2))

    ret = bytes([a ^ b for a, b in zip(input1[:shorter], input2[:shorter])])
    return ret

def generate_plaintext() -> bytes:
    plaintext = b'A'*14
    plaintext = urandom(randrange(0, 50)) + plaintext

    return plaintext

def encrypt(plaintext: bytes, mt19937_32_seed: int) -> bytes:    
    rng = MT19937_32(mt19937_32_seed)

    ciphertext = b""
    # 4 because mt19937's output is 4 bytes number
    for i in range(0, len(plaintext), 4):
        key = rng.extract_number()
        ciphertext += stream_xor(plaintext[i: i + 4], struct.pack("I", key))

    return ciphertext

def decrypt(ciphertext: bytes, mt19937_32_seed: int) -> bytes:
    rng = MT19937_32(mt19937_32_seed)

    plaintext = b""
    # 4 because mt19937's output is 4 bytes number
    for i in range(0, len(ciphertext), 4):
        key = rng.extract_number()
        plaintext += stream_xor(ciphertext[i: i + 4], struct.pack("I", key))

    return plaintext


def recover_seed(ciphertext: bytes):
    
    for i in range(0, 2**16):
        if b"A"*14 in decrypt(ciphertext, i):
            return i

if __name__ == "__main__":
    # random 16 bit seed
    consistent_but_unknown_seed = randrange(0, 2**16)
    print(f"used seed: {consistent_but_unknown_seed}")

    plaintext = generate_plaintext()
    ciphertext = encrypt(plaintext, consistent_but_unknown_seed)

    # tìm lại seed từ ciphertext
    start_time = time()
    recovered_seed = recover_seed(ciphertext)
    print(f"recovered seed: {recovered_seed}")
    print(f"{time() - start_time} seconds")