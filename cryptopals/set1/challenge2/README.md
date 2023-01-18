# **[set 1 - challenge 2](https://cryptopals.com/sets/1/challenges/2): Fixed XOR**
## XOR
### Khái niệm
XOR is a bitwise operator, and it stands for "exclusive or." It performs logical operation. If input bits are the same, then the output will be false(0) else true(1).
### Bảng chân lý
| A| B | A XOR B|
|- | - | :-----:|
| 0| 0 | 0      |
| 0| 1 | 1      |
| 1| 0 | 1      |
| 1| 1 | 0      |

## Challenge
Python script:
```
from binascii import unhexlify

input1 = unhexlify('1c0111001f010100061a024b53535009181c')
input2 = unhexlify('686974207468652062756c6c277320657965')
expected_result = unhexlify('746865206b696420646f6e277420706c6179')

output = []
for i in range(len(input1)):
    output.append(input1[i] ^ input2[i])

print(bytes(output) == expected_result)
```
Trong đó, unhexlify có chức năng là chuyển đổi string biểu diễn đưới dạng hexadecimal về dữ liệu kiểu binary: [detailed](../README.md)

Result:
```
┌──(kali㉿kali)-[~/Documents/cryptopals]
└─$ python script.py
True
```

## Easter egg
Nếu ta print ra input2 và expected_result:
```
print(input2)
print(expected_result)
```
Output:
```
b"hit the bull's eye"
b"the kid don't play"
````

## References
