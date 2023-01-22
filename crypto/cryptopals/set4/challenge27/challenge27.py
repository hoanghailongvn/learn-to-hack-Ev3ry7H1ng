from mytool import stream_xor
from os import urandom
from Crypto.Cipher import AES

## server side
consistent_but_unknown_key = urandom(16)
encryptor = AES.new(consistent_but_unknown_key, AES.MODE_CBC, consistent_but_unknown_key)
decryptor = AES.new(consistent_but_unknown_key, AES.MODE_CBC, consistent_but_unknown_key)

challenge27_encrypt = encryptor.encrypt
challenge27_decrypt = decryptor.decrypt


# attacker side
def attack():
    # P_1, P_2, P_3
    plaintext = b"A"*16 + b"B"*16 + b"C"*16
    # C_1, C_2, C_3
    ciphertext = challenge27_encrypt(plaintext)

    # C_1, 0, C_1
    malicious_ciphertext = ciphertext[0:16] + b"\x00"*16 + ciphertext[0:16]
    # P'_1, P'_2, P'_3
    malicious_plaintext = challenge27_decrypt(malicious_ciphertext)

    # P'_1 xor P'_3
    key = stream_xor(malicious_plaintext[0:16], malicious_plaintext[32:48])
    
    # kiểm tra đáp án
    print(key == consistent_but_unknown_key)

if __name__ == "__main__":
    attack()

    



    