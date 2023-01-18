# **[set 1 - challenge 4](https://cryptopals.com/sets/1/challenges/4): Detect single-character XOR**

## Solutions

Same as challenge 3:

```text
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
    max_score = -inf
    target_line = -1
    key = -1
    b_plaintext = b''

    with open("./4.txt", "r") as file:
        
        for i, line in enumerate(file):
            temp_key, score, b_temp_plaintext = crack(unhexlify(line.strip()))
            if max_score < score:
                target_line = i + 1
                key = temp_key
                max_score = score
                b_plaintext = b_temp_plaintext
    
    print(f"line: {target_line}")
    print(f"key: {key}")
    print(f"score: {max_score}")
    print(f"plain text: {b_plaintext}")
```

Result:

```text
line: 171
key: 53
score: 5
plain text: b'Now that the party is jumping\n'
```

## References
