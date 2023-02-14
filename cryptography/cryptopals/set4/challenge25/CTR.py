from random import randint
from Crypto.Cipher import AES
import struct

# xor 2 bytes object theo cái ngắn hơn
def stream_xor(input1: bytes, input2: bytes) -> bytes:
    shorter = min(len(input1), len(input2))

    ret = bytes([a ^ b for a, b in zip(input1[:shorter], input2[:shorter])])
    return ret

# mã hóa aes(nonce|counter) để tạo ra key trong ctr mode
def generate_keystream(nonce: bytes, counter: int, key: bytes):
    cryptor = AES.new(key, AES.MODE_ECB)

    return cryptor.encrypt(nonce + struct.pack("Q", counter))

# encrypt/decrypt ctr mode
def CTR(message: bytes, key: bytes, nonce: bytes) -> bytes:
    ret = b""

    for counter in range(0, len(message)//16 + 1):
        keystream = generate_keystream(nonce, counter, key)
        ret += stream_xor(message[counter*16 : (counter+1)*16], keystream)

    return ret