# **[set 1 - challenge 3](https://cryptopals.com/sets/1/challenges/3): Single-byte XOR cipher**

The hex encoded string:

```hex
1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736
```

... has been XOR'd against a single character. Find the key, decrypt the message.

You can do this by hand. But don't: write code to do it for you.

How? Devise some method for "scoring" a piece of English plaintext. Character frequency is a good metric. Evaluate each output and choose the one with the best score.

## XOR cipher decrypt

If we xor the cipher text with the key again, we can get the plaintext, this is called decrypt.

(A ^ B) ^ B = A ^ B ^ B = A ^ 0 = A

## Score method

Because the keyspace is small, we can use brute force to try each key and observe the result.

But, when the keyspace is larger, we can't manually check the results one by one. We need a way to automatically score each result.

Based on the different possibilities of each character being used in English, we can use this possibility to score the results.

From [Frequency Analysis](https://inventwithpython.com/hacking/chapter20.html), we have a simple method to score a string using python:

[source code here](./freqAnalysis.py)

In this simple scoring function:

- Count the number of each letter in the sentence, get the 6 most appearing characters and the 6 least appearing characters.
- plus 1 with each `most appearing characters` is one of the characters in the string `ETAOIN` (6 most common letters in English).
- plus 1 with each `least appearing characters` is one of the characters in the string `VKJXQZ` (6 least common letters in English).

## Solutions

write python script:

- xor ciphertext with each key from 0 - 255
- remove xor-ed string that has non printable characters
- use the python code above to score

```python
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
```

Result:

```text
key: 88
score: 5
plaintext: b"Cooking MC's like a pound of bacon"
```

## References

- Frequency Analysis: <https://inventwithpython.com/hacking/chapter20.html>
