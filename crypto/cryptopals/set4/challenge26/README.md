# **[set 4 - challenge 26](https://cryptopals.com/sets/4/challenges/26): CTR bitflipping**

## Requirements
Đọc lại bài [Challenge16: CBC bitflipping](../../set2/challenge16/README.md)

Tóm tắt:
- input của người dùng sẽ được đặt vào giữa 2 string "comment1=cooking%20MCs;userdata=" và ";comment2=%20like%20a%20pound%20of%20bacon"
- input không được phép có "=" và ";"
- input sẽ được gửi cho server, server encrypt bằng CTR (challenge16 là CBC) và ciphertext được trả về cho người dùng

Mục tiêu:
- Chỉnh sửa ciphertext sao cho khi server decrypt thì plaintext sẽ xuất hiện ";admin=true"

## Implement
- Implement lại hàm AES CTR encryption đã sử dụng ở những bài trước: [source code](./CTR.py)
- server side:
```
## server side
consistent_but_unknown_key = random_bytes(16)
nonce = struct.pack("Q", 0)

def challenge26_encrypt(attacker_controlled: bytes):
    plaintext = b"comment1=cooking%20MCs;userdata=" + attacker_controlled.replace(b'=', b'').replace(b';', b'') + b";comment2=%20like%20a%20pound%20of%20bacon"

    ciphertext = CTR.CTR(plaintext, consistent_but_unknown_key, nonce)
    return ciphertext

def challenge26_decrypt(ciphertext: bytes):
    plaintext = CTR.CTR(ciphertext, consistent_but_unknown_key, nonce)

    return plaintext
```

## Ý tưởng
"Thay đổi plaintext", "quan sát ciphertext tương ứng", "CTR mode", giống hệt [challenge25](../challenge25/README.md)

Sử dụng thuật toán như [challenge25](../challenge25/README.md), quan sát keystream ở vùng mình thay đổi được, chỉnh sửa ciphertext ở đó sao cho khi keystream xor ciphertext = plaintext có ";admin=true"

## Code
- attack():
```
# attacker side
def attack():
    payload = b";admin=true"

    # input của người dùng được đặt vào vị trí 32 trong plaintext
    # lấy keystream trong ở vị trí [32:32+len(payload)]
    ciphertext = challenge26_encrypt(b"\x00"*len(payload))
    # tính payload được encrypt bằng cách xor với keystream
    encrypted_payload = stream_xor(payload, ciphertext[32:32+len(payload)])
    malicious_ciphertext = ciphertext[:32] + encrypted_payload + ciphertext[32 + len(encrypted_payload):]

    print(success(malicious_ciphertext))
```
- Trong đó, hàm success() để kiểm tra ciphertext mà attack() tạo ra:
```
def success(ciphertext: bytes):
    return b";admin=true" in challenge26_decrypt(ciphertext)
```
Kết quả:
```
True
```
## References

