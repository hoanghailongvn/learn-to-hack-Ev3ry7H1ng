import base64
from Crypto.Cipher import AES
import struct

# xor 2 bytes object theo cái ngắn hơn
def stream_xor(input1: bytes, input2: bytes) -> bytes:
    shorter = min(len(input1), len(input2))

    ret = bytes([a ^ b for a, b in zip(input1[:shorter], input2[:shorter])])
    return ret

blocksize = 16

def generate_keystream(nonce: bytes, counter: int, key: bytes):
    cryptor = AES.new(key, AES.MODE_ECB)

    return cryptor.encrypt(nonce + struct.pack("Q", counter))

def CTR_decrypt(ciphertext: bytes, key: bytes, nonce: bytes) -> bytes:
    plaintext = b""

    for counter in range(0, len(ciphertext)//blocksize + 1):
        keystream = generate_keystream(nonce, counter, key)
        plaintext += stream_xor(ciphertext[counter*blocksize : (counter+1)*blocksize], keystream)

    return plaintext

if __name__ == "__main__":
    ciphertext = b"L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ=="
    ciphertext = base64.b64decode(ciphertext)
    key = b"YELLOW SUBMARINE"

    plaintext = CTR_decrypt(ciphertext, key, bytes(blocksize//2))
    print(plaintext)