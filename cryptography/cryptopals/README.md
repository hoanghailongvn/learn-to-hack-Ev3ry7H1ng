# [Cryptopals](https://cryptopals.com/)

Cryptopals is a collection of exercises that demonstrate attacks on real-world crypto.

These are my writeups for the cryptopals series.

[set1](./set1/):

- [challenge1: Convert hex to base64](./set1/challenge1/)
  - base64
  - xxd command
- [challenge2: Fixed XOR](./set1/challenge2/)
  - XOR operator
  - python: binascii.hexlify function
- [challenge3: Single-byte XOR cipher](./set1/challenge3/)
  - scoring plaintext function
- [challenge4: Detect single-character XOR](./set1/challenge4/)
  - use the challenge 3 function to find the key of a xored ciphertext.
- [challenge5: Implement repeating-key XOR](./set1/challenge5/)
  - repeating-key XOR
- [challenge6: Break repeating-key XOR](./set1/challenge6/)
  - hamming distance
- [challenge7: AES in ECB mode](./set1/challenge7/)
  - block cipher
  - AES: Advanced Encryption Standard
  - ECB: Electronic Code Block
- [challenge8: Detect AES in ECB mode](./set1/challenge8/)
  - detect ECB mode by counting the number of occurrences of each block

[set2](./set2/):

- [challenge9: Implement PKCS#7 padding](./set2/challenge9/)
  - padding in block cipher
  - PKCS#7
- [challenge10: Implement CBC mode](./set2/challenge10/)
  - block cipher
  - CBC: Cypher block chaining
- [challenge11: An ECB/CBC detection oracle](./set2/challenge11/)
  - how to detect blockcipher mode if we can control the input and observe the output
  - oracle
- [challenge12: Byte-at-a-time ECB decryption (Simple)](./set2/challenge12/)
  - find blocksize in block cipher
  - detect ECB mode
  - extracting what is appended after our input to a AES ECB encryption function if the key is consistent and we can observe the output
- [challenge13: ECB cut-and-paste](./set2/challenge13/)
  - exploit the inherent weakness of ECB mode: two identical plaintext - two identical ciphertext
  - fake cookie
- [challenge14: Byte-at-a-time ECB decryption (Harder)](./set2/challenge14/)
  - harder version of challenge 12
- [challenge15: PKCS#7 padding validation](./set2/challenge15/)
  - PKCS#7 padding validation written in python
- [challenge16: CBC bitflipping attacks](./set2/challenge16/)

[set3](./set3/):

- [challenge17: The CBC padding oracle](./set3/challenge17/)
- [challenge18: Implement CTR, the stream cipher mode](./set3/challenge18/)
- [challenge19: Break fixed-nonce CTR mode using substitutions](./set3/challenge19/)
- [challenge20: Break fixed-nonce CTR statistically](./set3/challenge20/)
- [challenge21: Implement the MT19937 Mersenne Twister RNG](./set3/challenge21/)
- [challenge22: Crack an MT19937 seed](./set3/challenge22/)
- [challenge23: Clone an MT19937 RNG from its output](./set3/challenge23/)
- [challenge24: Create the MT19937 stream cipher and break it](./set3/challenge24/)

[set4](./set4/):

- [challenge25: Break "random access read/write" AES CTR](./set4//challenge25/)
- [challenge26: CTR bitflipping](./set4//challenge26/)
- [challenge27: Recover the key from CBC with IV=Key](./set4//challenge27/)
- [challenge28: Implement a SHA-1 keyed MAC](./set4//challenge28/)
  - SHA-1
  - MAC
- [challenge29: Break a SHA-1 keyed MAC using length extension](./set4//challenge29/)
  - SHA-1 keyd MAC length extension attack
- [challenge30: Break an MD4 keyed MAC using length extension](./set4//challenge30/)
  - MD4 keyd MAC length extension attack
- [challenge31: Implement and break HMAC-SHA1 with an artificial timing leak](./set4//challenge31/)
  - HMAC-SHA1
  - timing leak attack
- [challenge32: Break HMAC-SHA1 with a slightly less artificial timing leak](./set4//challenge32/)
  - harder version of challenge 31

[set5](./set5/):

- [challenge33: Implement Diffie-Hellman](./set5/challenge33/)
  - Diffie-Hellman
  - Implement in python
- [challenge34: Implement a MITM key-fixing attack on Diffie-Hellman with parameter injection](./set5/challenge34/)
  - mitm: change A and B to p
- [challenge35: Implement DH with negotiated groups, and break with malicious "g" parameters](./set5/challenge35/)
  - mitm: change g to:
    - 1
    - p
    - p - 1
- [challenge36: Implement Secure Remote Password (SRP)](./set5/challenge36/)
- [challenge37: Break SRP with a zero key](./set5/challenge37/)
- [challenge38: Offline dictionary attack on simplified SRP](./set5/challenge38/)
- [challenge39: Implement RSA](./set5/challenge39/)
  - RSA
- [challenge40: Implement an E=3 RSA Broadcast attack](./set5/challenge40/)
  - Broadcast attack
  - CRT: Chinese remainder theorem
