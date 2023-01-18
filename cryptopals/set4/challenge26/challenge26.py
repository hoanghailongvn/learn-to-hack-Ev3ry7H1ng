import CTR
from CTR import stream_xor
from os import urandom
import struct

## server side
consistent_but_unknown_key = urandom(16)
nonce = struct.pack("Q", 0)

def challenge26_encrypt(attacker_controlled: bytes):
    plaintext = b"comment1=cooking%20MCs;userdata=" + attacker_controlled.replace(b'=', b'').replace(b';', b'') + b";comment2=%20like%20a%20pound%20of%20bacon"

    ciphertext = CTR.CTR(plaintext, consistent_but_unknown_key, nonce)
    return ciphertext


def challenge26_decrypt(ciphertext: bytes):
    plaintext = CTR.CTR(ciphertext, consistent_but_unknown_key, nonce)

    return plaintext

def success(ciphertext: bytes):
    return b";admin=true" in challenge26_decrypt(ciphertext)

# attacker side
def attack():
    payload = b";admin=true"

    # input của người dùng được đặt vào vị trí 32 trong plaintext
    # lấy keystream trong ở vị trí [32:32+len(payload)]
    ciphertext = challenge26_encrypt(b"\x00"*len(payload))
    # tính payload được encrypt bằng cách xor với keystream
    encrypted_payload = stream_xor(payload, ciphertext[32:32+len(payload)])
    malicious_ciphertext = ciphertext[:32] + encrypted_payload + ciphertext[32 + len(encrypted_payload):]

    print(success(malicious_ciphertext))

if __name__ == "__main__":
    attack()

    



    