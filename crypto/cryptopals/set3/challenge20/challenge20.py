import base64
from cmath import inf
from os import urandom
import string
from Crypto.Cipher import AES
import struct
import freqAnalysis

# xor 2 bytes object theo cái ngắn hơn
def stream_xor(input1: bytes, input2: bytes) -> bytes:
    shorter = min(len(input1), len(input2))

    ret = bytes([a ^ b for a, b in zip(input1[:shorter], input2[:shorter])])
    return ret

blocksize = 16
consistent_but_unknown_key = urandom(16)
nonce = struct.pack("Q", 0)

def generate_keystream(nonce: bytes, counter: int, key: bytes):
    cryptor = AES.new(key, AES.MODE_ECB)

    return cryptor.encrypt(nonce + struct.pack("Q", counter))

# vì là mã hóa bằng xor, nên 2 quả trình encrypt, decrypt h

def CTR(message: bytes, key: bytes, nonce: bytes) -> bytes:
    ret = b""

    for counter in range(0, len(message)//blocksize + 1):
        keystream = generate_keystream(nonce, counter, key)
        ret += stream_xor(message[counter*blocksize : (counter+1)*blocksize], keystream)

    return ret

def cracking_single_xor(b_ciphertext: bytes):
    max_score = -inf
    b_final_plaintext = b""
    final_key = -1

    for key in range(256):
        b_temp_plaintext = bytes(c ^ key for c in b_ciphertext)

        # b'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c'
        b_string_printable = bytes(string.printable, 'ascii')

        if all(p in b_string_printable for p in b_temp_plaintext):
            s = freqAnalysis.englishFreqMatchScore(b_temp_plaintext.decode('ascii'))
            if max_score < s:
                final_key = key
                max_score = s
                b_final_plaintext = b_temp_plaintext

    return final_key, max_score, b_final_plaintext

def crack():
    with open("20.txt", "r") as file:
        b64_plaintext = bytes(file.read(), 'ascii')
        file.close()

    list_plaintext = b64_plaintext.strip(b"\n").split(b"\n")
    list_plaintext = [base64.b64decode(line) for line in list_plaintext]
    list_ciphertext = []
    for p in list_plaintext:
        list_ciphertext.append(CTR(p, consistent_but_unknown_key, nonce))

    ########################################################################
    # Bắt đầu, chúng ta có một list các ciphertext: list_ciphertext

    len_longest_ciphertext = min([len(line) for line in list_ciphertext])
    key = b""

    # Ghép tất cả các kí tự ở vị trí i của từng ciphertext thành một
    # Rồi xử lý như challenge3, single-byte xor
    for i in range(len_longest_ciphertext):
        a = b"".join([bytes([line[i]]) if i < len(line) else b"" for line in list_ciphertext])

        temp_key, _, _ = cracking_single_xor(a)
        key += bytes([temp_key])

    for ciphertext in list_ciphertext:
        print(stream_xor(key, ciphertext))

if __name__ == "__main__":
    crack()
