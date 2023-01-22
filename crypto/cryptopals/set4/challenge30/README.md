# **[set 4 - challenge 30](https://cryptopals.com/sets/4/challenges/30): Break an MD4 keyed MAC using length extension**

Second verse, same as the first, but use MD4 instead of SHA-1. Having done this attack once against SHA-1, the MD4 variant should take much less time; mostly just the time you'll spend Googling for an implementation of MD4.

You're thinking, why did we bother with this?

```text
Blame Stripe. In their second CTF game, the second-to-last challenge involved breaking an H(k, m) MAC with SHA1. Which meant that SHA1 code was floating all over the Internet. MD4 code, not so much.
```

## Analysis

Breaking MD4 is almost the same as breaking SHA-1, here's the difference:

- in SHA1 algorithm we have h0, h1, ..., h4, then in MD4 we have A, B, C, D
- SHA1 output length: 20-byte, MDE output length: 16-byte
- SHA1: big endian, MD4: little endian

## Implement MD4

<https://gist.github.com/kangtastic/c3349fc4f9d659ee362b12d7d8c639b6>

## Break

because of this implementation MD4 don't have the \__padding() like the sha1 in the previous challenge, we rewrite this __padding() for convenient:

```python
@staticmethod
def __padding(stream):
    ml = len(stream) * 8
    stream += b"\x80"
    stream += b"\x00" * (-(len(stream) + 8) % 64)
    # little endian
    stream += struct.pack("<Q", ml)

    return stream
```

break: read [challenge 29](../challenge29/) for more detail

```python
def length_extension_attack(self, hash_value: bytes, message_length: int, new_text: bytes):
    # break hash_value into A, B, C, D
    for i in range(len(self.h)):
        self.h[i] = int.from_bytes(hash_value[i*4 : (i+1)*4], byteorder='little')

    # get the length of original message after padded
    previous_length = len(MD4.__padding(b'a'*message_length))

    # padding new_text, length of new message written to last 8 bytes
    # "<Q": little endian
    stream = MD4.__padding(new_text)
    stream = stream[0: -8] + struct.pack("<Q", (previous_length + len(new_text))*8)

    self._process([stream[i : i + 64] for i in range(0, len(stream), 64)])

    return self.hexdigest()
```

check:

```python
if __name__ == "__main__":
    recv = md4_mac(b"comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon")
    
    h = MD4()
    # 77 is the length of original message
    malicious_hash_value = h.length_extension_attack(recv, 77, b";admin=true")


    # check
    malicious_messsage = b'prefixcomment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x98\x02\x00\x00\x00\x00\x00\x00'
    malicious_messsage = malicious_messsage + b';admin=true'
    h = MD4(malicious_messsage)

    print(malicious_messsage)
    print(h.hexdigest())
    print(malicious_hash_value)
    print(h.hexdigest() == malicious_hash_value)
```

result:

```python
b'prefixcomment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x98\x02\x00\x00\x00\x00\x00\x00;admin=true'
e6abdc64dac6fea03578ea2bc6464ccf
e6abdc64dac6fea03578ea2bc6464ccf
True
```

## References

- MD4:
  - <https://datatracker.ietf.org/doc/html/rfc1320>
