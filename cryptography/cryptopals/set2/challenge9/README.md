# **[set 2 - challenge 9](https://cryptopals.com/sets/2/challenges/9): Implement PKCS#7 padding**

A block cipher transforms a fixed-sized block (usually 8 or 16 bytes) of plaintext into ciphertext. But we almost never want to transform a single block; we encrypt irregularly-sized messages.

One way we account for irregularly-sized messages is by padding, creating a plaintext that is an even multiple of the blocksize. The most popular padding scheme is called PKCS#7.

So: pad any block to a specific block length, by appending the number of bytes of padding to the end of the block. For instance,

```text
"YELLOW SUBMARINE"
```

... padded to 20 bytes would be:

```text
"YELLOW SUBMARINE\x04\x04\x04\x04"
```

## Padding

In a block cipher, when the plaintext size is not divisible by `blocksize`, it is necessary to use padding to add to the end of the plaintext.

## PKCS#7

PKCS7 padding works by adding `N` bytes with the value N, where N is the number of bytes needed to add to the message to complete the last block.

If the plaintext size is already divisible by `blocksize`, then N = `blocksize` (not 0)

Example:

message length is 16: "YELLOW SUBMARINE"

=> "YELLOW SUBMARINE\x04\x04\x04\x04"

## Challenge

Python code:

```python
def pkcs7(message: bytes, length: int) -> bytes:
    diff = length - len(message)
    padding = bytes([diff]*diff)

    ret = message + padding

    return ret

if __name__ == "__main__":
    message = b"YELLOW SUBMARINE"
    print(pkcs7(message, 20))
```

result:

```text
b'YELLOW SUBMARINE\x04\x04\x04\x04'
```

## References
