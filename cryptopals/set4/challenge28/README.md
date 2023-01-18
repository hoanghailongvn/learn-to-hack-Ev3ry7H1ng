# **[set 4 - challenge 28](https://cryptopals.com/sets/4/challenges/28): Implement a SHA-1 keyed MAC**

## Hash function
Hash function: tiếng việt gọi là `hàm băm`. Dùng để biến đổi đầu vào là nội dung có kích thước bất kì thành đầu ra có độ dài cố định.

Một trong những đặc điểm nổi bật của hàm băm là `không thể đảo ngược`.

## SHA-1
SHA-1 là viết tắt của Secure Hash Algorithm 1.

Là một hash function có output là 160 bit (20 bytes).

## MAC
MAC là viết tắt của Message authentication Secret.

Là phần thông tin dùng để đảm bảo message gửi đi không bị thay đổi trên đường truyền.

## Challenge28
Dùng sha1 ở đây : https://github.com/pcaro90/Python-SHA1/blob/master/SHA1.py

Viết thêm hàm theo challenge28:
```
def sha1_mac(message: bytes):
    h = SHA1()
    h.update(b"prefix" + message)
    return unhexlify(h.hexdigest())
```
Test:
```
if __name__ == "__main__":
    print(sha1_mac(b"long"))
```
Kết quả:
```
b'e\xcb\x8c\xdb\x17$\xd4\xea\x06\\\xa7\x05xp\x93\xd3F\x9cem'
```

## References
- Hash function: 
    - https://codelearn.io/sharing/hash-la-gi-va-hash-dung-de-lam-gi
    - https://en.wikipedia.org/wiki/Hash_function#Overview
- SHA-1:
    - https://en.wikipedia.org/wiki/SHA-1
- MAC:
    - https://en.wikipedia.org/wiki/Message_authentication_code