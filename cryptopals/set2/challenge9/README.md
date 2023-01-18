# **[set 2 - challenge 9](https://cryptopals.com/sets/2/challenges/9): Implement PKCS#7 padding**

## Padding
Block cipher thông thường sẽ mã hóa các blocks có kích thước cố định (như 8 bytes hoặc 16 bytes).

Do đó khi message có kích thước bị lẻ (không chia hết cho blocksize) thì cần sử dụng padding, thêm các ký tự khác vào cuối message để tạo thành đủ blocks.

## PKCS#7
PKCS7 padding hoạt động bằng cách thêm `N` bytes với giá trị N, trong đó N là số bytes cần thiết thêm vào message để hoàn thành block cuối.

Nếu độ dài message đã chia hết cho block thì N = blocksize (chứ không phải bằng 0)

Ví dụ như đề bài đã cho:

message: "YELLOW SUBMARINE"\
padding lên 20 bytes cần 4 bytes nữa\
=> "YELLOW SUBMARINE\x04\x04\x04\x04"

## Challenge
Python code:
```
def pkcs7(message: bytes, length: int) -> bytes:
    diff = length - len(message)
    padding = bytes([diff]*diff)

    ret = message + padding

    return ret

if __name__ == "__main__":
    message = b"YELLOW SUBMARINE"
    print(pkcs7(message, 20))
```
Kết quả:
```
b'YELLOW SUBMARINE\x04\x04\x04\x04'
```
## References
