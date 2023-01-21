import hashlib
from random import randrange
from os import urandom
import struct
from typing import Tuple

from Crypto.Cipher import AES

def sha1(message: bytes) -> bytes:
    h = hashlib.sha1()
    h.update(message)
    return h.digest()

def pkcs7(message: bytes, blocksize: int = 16) -> bytes:
    diff = blocksize - len(message) % blocksize

    padding = bytes([diff]*diff)

    ret = message + padding
    return ret

def pkcs7_padding_validate(message: bytes, blocksize: int = 16) -> bool:
    pad = message[-1]
    return message[-pad:] == bytes([pad]*pad)

def pkcs7_unpadding(message:bytes, blocksize: int = 16) -> bytes:
    pad = message[-1]
    return message[: -pad]

##########################################################################

def aes_cbc_encrypt(key: bytes, iv: bytes, pt: bytes):
    cryptor = AES.new(key, AES.MODE_CBC, iv)
    return cryptor.encrypt(pkcs7(pt))

def aes_cbc_decrypt(key: bytes, iv: bytes, ct: bytes):
    cryptor = AES.new(key, AES.MODE_CBC, iv)

    return pkcs7_unpadding(cryptor.decrypt(ct))

class A:
    def __init__(self):
        self.p = 37
        self.g = 5
        self.A = None

        self._a = randrange(0, self.p)
        self._s = None
        self._key = None

    def send_p_g_A(self) -> Tuple[bytes, bytes, bytes]:
        # A = (g**a) % p
        self.A = pow(self.g, self._a, self.p)
        message = (self.p, self.g, self.A)

        print(f"A send: p g A: {message}")
        return message

    def recv_B(self, B_):
        # s = (B**a) % p
        self._s = pow(B_, self._a, self.p)
        self._key = sha1(self._s.to_bytes(256, byteorder='big'))[:16]

        print(f"A recv: B: {B_}")
        print(f"A s: {self._s}")
        print(f"A key: {self._key}")

    def send(self) -> Tuple[bytes, bytes]:
        pt = b"private message"
        iv = urandom(16)
        ct = aes_cbc_encrypt(self._key, iv, pt)

        print(f"A send: {pt}")
        return ct, iv
    def recv(self, message):
        ct, iv = message
        pt = aes_cbc_decrypt(self._key, iv, ct)

        print(f"A received: {pt}")
    
class B:
    def __init__(self) -> None:
        self.p = None
        self.g = None
        self.B = None
       
        self._b = None
        self._s = None
        self._key = None

    def recv_p_g_A(self, message: Tuple[bytes, bytes, bytes]) -> bytes:
        self.p, self.g, A_ = message
        self._b = randrange(0, self.p)

        # s = (A**b) % p
        self._s = pow(A_, self._b, self.p)
        self._key = sha1(self._s.to_bytes(256, byteorder='big'))[:16]

        # B = (g**b) % p
        self.B = pow(self.g, self._b, self.p)

        print(f"B received p g a: {message}")
        print(f"B s: {self._s}")
        print(f"B key: {self._key}")
        print(f"B send B: {self.B}")
        return self.B

    def send(self) -> Tuple[bytes, bytes]:
        pt = b"private message"
        iv = urandom(16)
        ct = aes_cbc_encrypt(self._key, iv, pt)

        print(f"B send: {pt}")
        return ct, iv

    def recv(self, message):
        ct, iv = message
        pt = aes_cbc_decrypt(self._key, iv, ct)

        print(f"B received: {pt}")

def simulate():
    alice = A()
    bob = B()

    p_g_A = alice.send_p_g_A()
    B_ = bob.recv_p_g_A(p_g_A)
    alice.recv_B(B_)

    message = alice.send()
    bob.recv(message)

def simulate_mitm():
    alice = A()
    bob = B()

    p_g_A = alice.send_p_g_A()

    # p g=1 A
    fake_p_g_A = (p_g_A[0], ) + (1, ) + (p_g_A[2], )

    # B=1
    B_ = bob.recv_p_g_A(fake_p_g_A)
    alice.recv_B(B_)

    # => A-side: s = 1
    message = alice.send()

    # mitm
    ct, iv = message
    pt = aes_cbc_decrypt(sha1((1).to_bytes(256, byteorder='big'))[:16], iv, ct)
    print(f"MITM: {pt}")

if __name__ == "__main__":
    simulate_mitm()