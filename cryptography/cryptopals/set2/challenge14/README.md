# **[set 2 - challenge 14](https://cryptopals.com/sets/2/challenges/14): Byte-at-a-time ECB decryption (Harder)**

Take your oracle function [from #12](./../challenge12/). Now generate a random count of random bytes and prepend this string to every plaintext. You are now doing:

```text
AES-128-ECB(random-prefix || attacker-controlled || target-bytes, random-key)
```

Same goal: decrypt the target-bytes.

## Analysis

The difference compared with challenge 12 is that the random-prefix prepend before your controllable input.

To make this no difference to challenge 12, we need to know the length of the prefix and padding so that `prefix + pad` is divisible by blocksize

## Solution

padding the prefix:

- we already know that blocksize = 16, ecb mode
- with the prefix fixed in first position, infer that already have >= 0 ciphertext block has been fixed.
- enter `attacker-controlled` with increasing length, until there is one more fixed ciphertext block

    ```python
    def find_len_prefix():
        # i == 0
        ciphertext = AES_encrypt_ECB_mode(b"")
        # Split the ciphertext into 16-byte blocks and put them in a list
        twoprev_ciphertext_block16 = [ciphertext[j:j+blocksize] for j in range(0, len(ciphertext), blocksize)]

        # i == 1
        ciphertext = AES_encrypt_ECB_mode(b"a")
        # Split the ciphertext into 16-byte blocks and put them in a list
        prev_ciphertext_block16 = [ciphertext[j:j+blocksize] for j in range(0, len(ciphertext), blocksize)]

        # Find the fixed number of blocks
        nb_fixed_block = 0
        for i in range(len(twoprev_ciphertext_block16)):
            if twoprev_ciphertext_block16[i] == prev_ciphertext_block16[i]:
                nb_fixed_block += 1
            else:
                break

        # increase attacker_controlled length to blocksize * 2 until a new fixed ciphểtxt block appears
        for i in range(2, blocksize * 2):
            attacker_controlled = bytes('a'*i, 'ascii')
            ciphertext = AES_encrypt_ECB_mode(attacker_controlled)
            ciphertext_block16 = [ciphertext[j:j+blocksize] for j in range(0, len(ciphertext), blocksize)]

            if ciphertext_block16[nb_fixed_block] == prev_ciphertext_block16[nb_fixed_block]:
                nb_fixed_block += 1
                return nb_fixed_block * blocksize - (i - 1)
            else:
                prev_ciphertext_block16 = ciphertext_block16
    ```

The rest is the same as [challenge 12](../challenge12/):

```python
def crack():
    # b'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c'
    printable = string.printable

    len_target_bytes = 144
    target_bytes = ''

    len_prefix = fine_len_prefix()
    # pad prefix
    len_append_to_prefix = blocksize - len_prefix % blocksize
    if len_append_to_prefix == blocksize:
        len_append_to_prefix = 0
    
    # the block where the bruteforce happened
    block_start = 128 + len_prefix + len_append_to_prefix
    block_end = 144 + len_prefix + len_append_to_prefix

    for i in range(len_target_bytes):
        attacker_controlled = bytes('a'*(len_append_to_prefix + len_target_bytes - i - 1), 'ascii')
        ciphertext = AES_encrypt_ECB_mode(attacker_controlled)

        for c in printable:
            brute_force_attacker_controlled = attacker_controlled + bytes(target_bytes, 'ascii') + bytes(c, 'ascii')
            brute_force_ciphertext = AES_encrypt_ECB_mode(brute_force_attacker_controlled)
            if brute_force_ciphertext[block_start:block_end] == ciphertext[block_start:block_end]:
                target_bytes += c
                break
    return target_bytes
```

result:

```text
Rollin' in my 5.0
With my rag-top down so my hair can blow
The girlies on standby waving just to say hi
Did you stop? No, I just drove by
```

Source code: [here](./challenge14.py)

## References
