# **[set 4 - challenge 27](https://cryptopals.com/sets/4/challenges/27): Recover the key from CBC with IV=Key**


## Đề bài
Đề bài cho ta sử dụng hàm encrypt(), decrypt() AES CBC với consistent_but_unknown_key, điểm đặc biệt ở đây là dùng luôn key làm iv cho CBC mode.

Mục tiêu là tìm consistent_but_unknown_key.

## Ý tưởng
Gợi ý của đề bài:
- encrypt plaintext gồm 3 block P_1, P_2, P_3
```
AES-CBC(P_1, P_2, P_3) -> C_1, C_2, C_3
```
- decrypt ciphertext gồm 3 block C_1, 0, C_1
```
C_1, C_2, C_3 -> C_1, 0, C_1
```
- lấy block thứ 1 xor với block thứ 3 của plaintext mới
```
P'_1 XOR P'_3
```

Cùng xem lại sơ đồ CBC encrypt và decrypt:

<img src="pictures/CBC_e.png">

<img src="pictures/CBC_d.png">

Phân tích:
- C_1 = E(P_1 ^ key)
- P'_1 = D(C_1) ^ vi = P_1 ^ key ^ key = P_1
- P'_3 = D(C_1) ^ C_2 = P_1 ^ key ^ 0 = P_1 ^ key

=> P'_1 ^ P'_3 = key

## Code
<!-- - Implement lại CBC với vi = key: [source code here](./CBC.py) -->
- Phía server để key cố định:
```
## server side
consistent_but_unknown_key = random_bytes(16)
cryptor = AES.new(consistent_but_unknown_key, AES.MODE_CBC, consistent_but_unknown_key)

challenge27_encrypt = cryptor.encrypt
challenge27_decrypt = cryptor.decrypt
```
- Thuật toán tìm key như đề bài:
```
# attacker side
def attack():
    # P_1, P_2, P_3
    plaintext = b"A"*16 + b"B"*16 + b"C"*16
    # C_1, C_2, C_3
    ciphertext = challenge27_encrypt(plaintext)

    # C_1, 0, C_1
    malicious_ciphertext = ciphertext[0:16] + b"\x00"*16 + ciphertext[0:16]
    # P'_1, P'_2, P'_3
    malicious_plaintext = challenge27_decrypt(malicious_ciphertext)

    # P'_1 xor P'_3
    key = stream_xor(malicious_plaintext[0:16], malicious_plaintext[32:48])
    
    # kiểm tra đáp án
    print(key == consistent_but_unknown_key)
```
Kết quả:
```
True
```

## References
