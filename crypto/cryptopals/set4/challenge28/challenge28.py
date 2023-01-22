from sha1 import SHA1
from binascii import unhexlify


def sha1_mac(message: bytes):
    h = SHA1()
    h.update(b"prefix" + message)
    return unhexlify(h.hexdigest())

if __name__ == "__main__":
    print(sha1_mac(b"long"))
