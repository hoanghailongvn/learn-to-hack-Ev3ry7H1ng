from random import choice, randrange
from os import urandom
import hashlib
from typing import Tuple

N = 0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff
g = 2
k = 3
I = b"hoanghailong2642k@gmail.com"
P = b"123abc!@#"

# sha256 and hmac
def bxor(b1: bytes, b2: bytes) -> bytes: # use xor for bytes
    result = b""
    for b1, b2 in zip(b1, b2):
        result += bytes([b1 ^ b2])
    return result

def do_sha256(message: bytes) -> bytes:
    h = hashlib.sha256()
    h.update(message)
    return h.digest()

def hmac_sha256(message: bytes, key: bytes) -> bytes:
    ipad = b'\x36' * 64
    opad = b'\x5C' * 64

    if len(key) > 64:
        key = do_sha256(key)

    if len(key) < 64:
        key = key.ljust(64, b"\x00")

    return do_sha256(bxor(key, opad) + do_sha256(bxor(key, ipad) + message))

# ------------------------------------------------------------------------------

# class Server:
#     def __init__(self) -> None:
#         self.salt = urandom(8)
#         xH = do_sha256(self.salt + P)
#         x = int.from_bytes(xH, byteorder='big')
#         self.v = pow(g, x, N)
#         self._b = randrange(0, N)
#         self.B = pow(g, self._b, N)
#         self.u = int.from_bytes(urandom(16), byteorder='big')
#         self.S = None
#         self.K = None

#     def recv_I_A(self, message: Tuple[bytes, int]):
#         I_, A = message

#         self.S = pow(A * pow(self.v, self.u, N), self._b, N)
#         self.K = do_sha256(self.S.to_bytes(256, byteorder='big'))

#         # print(f"S: S = {self.S}")
#         # print(f"S: K = {self.K}")


#     def send_salt_B_u(self) -> Tuple[bytes, int, int]:
#         return (self.salt, self.B, self.u)

#     def recv_hmac(self, message: bytes) -> bytes:
#         if message == hmac_sha256(self.K, self.salt):
#             print(f"S: accept")
#             return b"OK"
#         return b"No no no"


class Client:
    def __init__(self, random_password: bytes) -> None:
        self._a = randrange(0, N)
        self.A = None
        self.S = None
        self.K = None
        self.salt = None
        self.random_password = random_password

    def send_I_A(self) -> Tuple[bytes, int]:
        self.A = pow(g, self._a, N)

        return (I, self.A)

    def recv_salt_B_u(self, message: Tuple[bytes, int, int]):
        self.salt, B, u = message

        xH = do_sha256(self.salt + self.random_password)
        x = int.from_bytes(xH, byteorder='big')

        self.S = pow(B, self._a + u * x, N)
        self.K = do_sha256(self.S.to_bytes(256, byteorder='big'))
    
    def send_hmac(self) -> bytes:
        return hmac_sha256(self.K, self.salt)
    
    def recv_result(self, message: bytes):
        print(message)

# def simulate():
#     s = Server()
#     c = Client()

#     # Client -> Server: I, A
#     I_A = c.send_I_A()
#     s.recv_I_A(I_A)

#     # Server -> Client: salt, B, u
#     salt_B_u = s.send_salt_B_u()
#     c.recv_salt_B_u(salt_B_u)

#     # Client -> Server: hmac
#     hmac_value = c.send_hmac()
#     result = s.recv_hmac(hmac_value)
#     c.recv_result(result)

def mitm_simulate():
    with open("10k-most-common.txt", "r") as file:
        passwords = file.read()
        file.close()

        expected_password = choice(passwords.split())
        print(f"expected password: {expected_password}")

        c = Client(bytes(expected_password, 'utf-8'))


    # Client -> Attacker: I, A
    _, A = c.send_I_A()

    # Attacker -> Client: salt, B, u
    b = randrange(0, N)
    B = pow(g, b, N)
    salt = urandom(8)
    u = randrange(0, pow(2, 128))

    c.recv_salt_B_u((salt, B, u))

    # Client -> Attacker: hmac
    hmac_value = c.send_hmac()
    
    # Attacker đã có hmac, chỉ cần tự tính hmac cho từng password và bruteforce thôi
    for password in passwords.split():
        b_password = bytes(password, 'utf-8')

        xH = do_sha256(salt + b_password)
        x = int.from_bytes(xH, byteorder='big')
        
        bruteforce_S = (pow(A, b, N) * pow(g, u*x*b, N)) % N
        bruteforce_K = do_sha256(bruteforce_S.to_bytes(256, byteorder='big'))

        bruteforce_hmac = hmac_sha256(bruteforce_K, salt)

        if bruteforce_hmac == hmac_value:
            print(f"Found password: {password}")
            break

if __name__ == "__main__":
    mitm_simulate()
    