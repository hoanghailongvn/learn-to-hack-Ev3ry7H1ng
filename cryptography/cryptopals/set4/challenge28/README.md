# **[set 4 - challenge 28](https://cryptopals.com/sets/4/challenges/28): Implement a SHA-1 keyed MAC**

Find a SHA-1 implementation in the language you code in.

Don't cheat. It won't work.

```text
Do not use the SHA-1 implementation your language already provides (for instance, don't use the "Digest" library in Ruby, or call OpenSSL; in Ruby, you'd want a pure-Ruby SHA-1).
```

Write a function to authenticate a message under a secret key by using a secret-prefix MAC, which is simply:

```text
SHA1(key || message)
```

Verify that you cannot tamper with the message without breaking the MAC you've produced, and that you can't produce a new MAC without knowing the secret key.

## SHA-1

In cryptography, SHA-1 (Secure Hash Algorithm 1) is a hash function which takes an input and produces a 160-bit (20-byte) hash value known as a message digest – typically rendered as 40 hexadecimal digits. ([wikipedia](https://en.wikipedia.org/wiki/SHA-1))

output: 160-bit, 20-byte, 40 hexadecimal digits.

Since 2005, SHA-1 has not been considered secure.

## MAC

MAC stands for Message authentication Secret.

The piece of information used to ensure that the message is not changed during transmission.

## Challenge28

source code for sha1 : <https://github.com/pcaro90/Python-SHA1/blob/master/SHA1.py>

write the sha1_mac function using the sha1 function:

```python
def sha1_mac(message: bytes):
    h = SHA1()
    h.update(b"prefix" + message)
    return unhexlify(h.hexdigest())
```

check:

```python
if __name__ == "__main__":
    print(sha1_mac(b"long"))
```

result:

```python
b'e\xcb\x8c\xdb\x17$\xd4\xea\x06\\\xa7\x05xp\x93\xd3F\x9cem'
```

## References

- Hash function:
  - <https://codelearn.io/sharing/hash-la-gi-va-hash-dung-de-lam-gi>
  - <https://en.wikipedia.org/wiki/Hash_function#Overview>
- SHA-1:
  - <https://en.wikipedia.org/wiki/SHA-1>
- MAC:
  - <https://en.wikipedia.org/wiki/Message_authentication_code>
