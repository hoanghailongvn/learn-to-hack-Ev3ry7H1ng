# **[set 2 - challenge 15](https://cryptopals.com/sets/2/challenges/15): PKCS#7 padding validation**

Write a function that takes a plaintext, determines if it has valid PKCS#7 padding, and strips the padding off.

The string:

```text
"ICE ICE BABY\x04\x04\x04\x04"
```

... has valid padding, and produces the result "ICE ICE BABY".

The string:

```text
"ICE ICE BABY\x05\x05\x05\x05"
```

... does not have valid padding, nor does:

```text
"ICE ICE BABY\x01\x02\x03\x04"
```

If you are writing in a language with exceptions, like Python or Ruby, make your function throw an exception on bad padding.

Crypto nerds know where we're going with this. Bear with us.

## Solution

```python
def pkcs7_padding_validate(input: bytes) -> bool:
    pad = input[-1]
    return input[-pad:] == bytes([pad]*pad)
```

check:

```python
if __name__ == "__main__":
    print(pkcs7_padding_validate(b"asdf\x04\x04\x04\x04"))
    print(pkcs7_padding_validate(b"asdf\x04\x04\x04\x05"))
```

result:

```text
True
False
```

## References
