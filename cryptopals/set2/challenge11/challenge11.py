from random import randint
from Crypto.Cipher import AES
from os import urandom

def pkcs7(message: bytes, blocksize: int) -> bytes:
    diff = blocksize - len(message) % blocksize

    padding = bytes([diff]*diff)

    ret = message + padding

    return ret

def append_5_10(plaintext: bytes):
    first = randint(5, 10)
    last = randint(5, 10)
    ret = urandom(first) + plaintext + urandom(last)

    return ret

# AES_encrypt with 50% ecb mode and 50% cbc mode
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

def detect_ECB(ciphertext: bytes, blocksize: int = 16):
    dict_cipher = {}
    for i in range(0, len(ciphertext), blocksize):
        blockk = ciphertext[i:i+blocksize]
        if blockk in dict_cipher:
            dict_cipher[blockk] += 1
        else:
            dict_cipher[blockk] = 1

    # In ra block nào xuất hiện nhiều hơn 1 lần
    for blockk in dict_cipher:
        if dict_cipher[blockk] > 1:
            print(f"block: {blockk}\ntimes: {dict_cipher[blockk]}")
            return True
    return False

if __name__ == "__main__":
    ciphertext = AES_encrypt(bytes("a"*42, 'ascii'))
    print(f"ciphertext: {ciphertext}")
    if detect_ECB(ciphertext):
        print("detected mode: ecb")
    else:
        print("detected mode: cbc")
    