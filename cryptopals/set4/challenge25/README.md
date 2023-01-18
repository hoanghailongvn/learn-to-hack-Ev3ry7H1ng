# **[set 4 - challenge 25](https://cryptopals.com/sets/4/challenges/25): Break "random access read/write" AES CTR**

## Đề bài
Hàm edit(offset, newtext), trả về ciphertext mới, mà trong đó plaintext dùng để encrypt đã được ghi đè bằng newtext ở vị trị offset.

Phía tấn công chỉ có được hàm edit() này, sử dụng nó để lấy được plaintext.

Mã hóa bằng AES, CTR.

## Implement
- Implement lại hàm AES CTR encryption đã sử dụng ở những bài trước: [source code](./CTR.py)
- edit():
```
import CTR
from CTR import random_bytes
import struct

## server side
consistent_but_unknown_key = random_bytes(16)
with open("25.txt", "r") as file:
    plaintext = bytes(file.read(), 'ascii')
    file.close()

nonce = struct.pack("Q", 0)
def edit(offset: int, newtext: bytes):
    new_plaintext = plaintext[:offset] \
                    + newtext \
                    + plaintext[offset + len(newtext):]

    return CTR.CTR(new_plaintext, consistent_but_unknown_key, nonce)
```

## Ý tưởng
Ngắm lại sơ đồ encrypt/decrypt CTR một chút:

<img src="pictures/ctr_e.png">

Ta có thể thấy ngay rằng, nếu ta có thể tùy ý thay đổi plaintext, quan sát được ciphertext, thì ta có thể tính ra keystream, với keystream = plaintext xor ciphertext.

## Code
```
# attacker side
def recover_plaintext():
    # original ciphertext and get length of plaintext = ciphertext
    original_ciphertext = edit(0, b"")
    len_plaintext = len(edit(0, b""))

    # Cho tất cả bytes trong plaintext về \x00, lúc này ciphertext chính là keystream
    keystream = edit(0, b"\x00" * len_plaintext)

    # keystream xor original_ciphertext = original plaintext
    original_plaintext = stream_xor(keystream, original_ciphertext)

    return original_plaintext

if __name__ == "__main__":
    recovered_plaintext = recover_plaintext()
    print(recovered_plaintext == plaintext)
```
Kết quả:
```
True
```

## References

