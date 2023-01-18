import base64
from cmath import inf
import string
import freqAnalysis

def hamming_distance(input1: bytes, input2: bytes):
    ret = 0
    
    for i in range(len(input1)):
        bin1 = f"{input1[i]:08b}"
        bin2 = f"{input2[i]:08b}"

        for j in range(8):
            if bin1[j] is not bin2[j]:
                ret += 1
    
    return ret

def repeating_key_xor(msg: bytes, key: bytes):
    ciphertext = []

    for i, c in enumerate(msg):
        ciphertext.append(msg[i] ^ key[i % len(key)])
    
    return bytes(ciphertext)

def score_KEYSIZE(ciphertext: bytes, KEYSIZE: int):
    max_nb_block = len(ciphertext) // KEYSIZE - 1
    
    score = 0
    for i in range(max_nb_block):
        score += hamming_distance(ciphertext[KEYSIZE * i: KEYSIZE * (i + 1)], ciphertext[KEYSIZE * (i + 1): KEYSIZE * (i + 2)])
    
    score /= KEYSIZE
    score /= max_nb_block

    return score

def guess_KEYSIZE(ciphertext: bytes, size_start=2, size_end=40):
    min = inf
    ret = -1
    for KEYSIZE in range(size_start, size_end):
        score = score_KEYSIZE(ciphertext, KEYSIZE)
        if min > score:
            min = score
            ret = KEYSIZE

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

def cracking_repeat_xor(ciphertext: bytes):
    guessed_keysize = guess_KEYSIZE(ciphertext)
    print(f"guessed keysize: {guessed_keysize}")

    key = []
    for i in range(guessed_keysize):
        temp_key, _, _ = cracking_single_xor((([ciphertext[c] for c in range(i, len(ciphertext), guessed_keysize)])))
        key.append(temp_key)

    return bytes(key), repeating_key_xor(ciphertext, bytes(key))

    print(bytes(key))
    print(repeating_key_xor(ciphertext, bytes(key)).decode())


if __name__ == "__main__":
    with open("6.txt", "r") as file:
        ciphertext = base64.b64decode(file.read())
        file.close()

        key, b_plaintext = cracking_repeat_xor(ciphertext)
        print(f"Key: {key}")
        print(f"Plaintext: \n{b_plaintext.decode()}")
