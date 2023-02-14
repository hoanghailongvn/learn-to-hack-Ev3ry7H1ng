from binascii import unhexlify
from cmath import inf
import string
import freqAnalysis

def crack(b_ciphertext: bytes):
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

if __name__ == "__main__":
    b_ciphertext = unhexlify(b'1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736')
    key, score, b_plaintext = crack(b_ciphertext)
    print(f"key: {key}\nscore: {score}\nplaintext: {b_plaintext}")