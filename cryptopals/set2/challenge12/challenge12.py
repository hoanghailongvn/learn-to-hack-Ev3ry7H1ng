import base64
from Crypto.Cipher import AES
import string
from os import urandom

def pkcs7(message: bytes, blocksize: int) -> bytes:
    diff = blocksize - len(message) % blocksize

    padding = bytes([diff]*diff)

    ret = message + padding
    return ret

consistent_but_unknown_key = urandom(16)
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

def find_blocksize():
    prev_first_two_bytes = AES_encrypt_ECB_mode(b'a')[:2]
    # `attacker_controlled` with increasing length
    for i in range(2, 100):
        first_two_bytes = AES_encrypt_ECB_mode(bytes('a'*i, 'ascii'))[:2]
        if prev_first_two_bytes == first_two_bytes:
            return i - 1
        else:
            prev_first_two_bytes = first_two_bytes

def is_ecb(blocksize: int = 16):
    attacker_controlled = bytes('a'*32, 'ascii')
    ciphertext = AES_encrypt_ECB_mode(attacker_controlled)
    if ciphertext[0:blocksize] == ciphertext[blocksize:blocksize*2]:
        return True
    else:
        return False

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

if __name__ == "__main__":
    cracked = crack()
    print(cracked)