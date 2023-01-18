# **[set 2 - challenge 15](https://cryptopals.com/sets/2/challenges/15): PKCS#7 padding validation**

## Solution
Hiểu cách PKCS#7, ta sẽ dễ dàng viết được hàm validation thôi:
```
def pkcs7_padding_validate(input: bytes) -> bool:
    pad = input[-1]
    return input[-pad:] == bytes([pad]*pad)
```
Kiểm tra:
```
if __name__ == "__main__":
    print(pkcs7_padding_validate(b"asdf\x04\x04\x04\x04"))
    print(pkcs7_padding_validate(b"asdf\x04\x04\x04\x05"))
```
Kết quả:
```
True
False
```

## References
