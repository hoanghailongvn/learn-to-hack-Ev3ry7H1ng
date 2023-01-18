from Crypto.Cipher import AES
from random import randint

# xor 2 bytes object có độ dài bằng nhau
def stream_xor(input1: bytes, input2: bytes) -> bytes:
    if len(input1) != len(input2):
        assert("stream_xor: length not equal!")

    ret = bytes([a ^ b for a, b in zip(input1, input2)])
    return ret

def pkcs7(message: bytes, blocksize: int) -> bytes:
    diff = blocksize - len(message) % blocksize
    padding = bytes([diff]*diff)
    ret = message + padding
    return ret

def pkcs7_unpadding(message:bytes) -> bytes:
    pad = message[-1]
    return message[: -pad]