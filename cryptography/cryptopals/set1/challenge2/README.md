# **[set 1 - challenge 2](https://cryptopals.com/sets/1/challenges/2): Fixed XOR**

Write a function that takes two equal-length buffers and produces their XOR combination.

If your function works properly, then when you feed it the string:

```text
1c0111001f010100061a024b53535009181c
```

... after hex decoding, and when XOR'd against:

```text
686974207468652062756c6c277320657965
```

... should produce:

746865206b696420646f6e277420706c6179

## XOR

XOR is a bitwise operator, and it stands for "exclusive or." It performs logical operation. If input bits are the same, then the output will be false(0) else true(1).

| A| B | A XOR B|
|- | - | :-----:|
| 0| 0 | 0      |
| 0| 1 | 1      |
| 1| 0 | 1      |
| 1| 1 | 0      |

## Solutions

Python script:

```text
from binascii import unhexlify

input1 = unhexlify('1c0111001f010100061a024b53535009181c')
input2 = unhexlify('686974207468652062756c6c277320657965')
expected_result = unhexlify('746865206b696420646f6e277420706c6179')

output = []
for i in range(len(input1)):
    output.append(input1[i] ^ input2[i])

print(bytes(output) == expected_result)
```

unhexlify: string represented in hexadecimal to binary data

Result:

```bash
┌──(kali㉿kali)-[~/Documents/cryptopals]
└─$ python script.py
True
```

## Easter egg

If we print the contents of input2 and expected_result:

```text
print(input2)
print(expected_result)
```

Output:

```text
b"hit the bull's eye"
b"the kid don't play"
````

## References

[binascii.unhexlify](https://docs.python.org/3/library/binascii.html#binascii.unhexlify)
