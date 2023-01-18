# **[set 4 - challenge 30](https://cryptopals.com/sets/4/challenges/30): Break an MD4 keyed MAC using length extension**

Break giống như với SHA-1, điểm khác biệt:
- SHA1 có h0, h1, ..., h4 tổng là 20 byte, thì MD4 chỉ có A, B, C, D tổng là 16 byte. đây cũng chính là độ dài hash value của MD4
- SHA1 là big endian, MD4 là little endian

## Implement MD4
https://gist.github.com/kangtastic/c3349fc4f9d659ee362b12d7d8c639b6

## Code
Do implementation MD4 này không có hàm __padding() như sha1 trong challenge trước, ta viết lại hàm __padding() cho tiện sử dụng:
```
@staticmethod
def __padding(stream):
    ml = len(stream) * 8
    stream += b"\x80"
    stream += b"\x00" * (-(len(stream) + 8) % 64)
    stream += struct.pack("<Q", ml)

    return stream
```

Tương tự như challenge 28, chỉ cần thay đổi thành little endian:
```
def length_extension_attack(self, hash_value: bytes, message_length: int, new_text: bytes):
    # break hash_value into A, B, C, D
    for i in range(len(self.h)):
        self.h[i] = int.from_bytes(hash_value[i*4 : (i+1)*4], byteorder='little')

    # sử dụng hàm __padding để lấy độ dài của message cũ
    previous_length = len(MD4.__padding(b'a'*message_length))

    # sử dụng hàm __padding để padding new_text, thay 8 bytes ở cuối thành độ dài mới
    # Khác với SHA1 ở "<Q" nghĩa là little endian
    stream = MD4.__padding(new_text)
    stream = stream[0: -8] + struct.pack("<Q", (previous_length + len(new_text))*8)

    self._process([stream[i : i + 64] for i in range(0, len(stream), 64)])

    return self.hexdigest()
```
Kiểm tra:
```
if __name__ == "__main__":
    recv = md4_mac(b"comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon")
    
    h = MD4()
    # coi như đã biết độ dài của message ban đầu là 6 + 77 = 83
    malicious_hash_value = h.length_extension_attack(recv, 83, b";admin=true")


    # Kiểm tra
    malicious_messsage = b'prefixcomment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x98\x02\x00\x00\x00\x00\x00\x00'
    malicious_messsage = malicious_messsage + b';admin=true'
    h = MD4(malicious_messsage)

    print(malicious_messsage)
    print(h.hexdigest())
    print(malicious_hash_value)
    print(h.hexdigest() == malicious_hash_value)
```
Kết quả:
```
b'prefixcomment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x98\x02\x00\x00\x00\x00\x00\x00;admin=true'
e6abdc64dac6fea03578ea2bc6464ccf
e6abdc64dac6fea03578ea2bc6464ccf
True
```

## References
- MD4:
    - https://datatracker.ietf.org/doc/html/rfc1320