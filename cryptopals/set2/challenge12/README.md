# **[set 2 - challenge 12](https://cryptopals.com/sets/2/challenges/12): Byte-at-a-time ECB decryption (Simple)**

## Đề bài
Viết hàm mã hóa AES128 mode ECB:

AES-128-ECB(attacker-controlled || target-bytes, random-key)

Trong đó:
- attacker-controlled: phần plaintext mình thích làm gì thì làm
- target-bytes: mục tiêu cần tìm
- random-key: consistent_but_unknown_key

## Hàm oracle AES
- python code:
```
import base64
from random import randint
from Crypto.Cipher import AES

def random_bytes(length: int) -> bytes:
    ret = []
    for _ in range(length):
        ret.append(randint(0, 255))
    
    return bytes(ret)

consistent_but_unknown_key = random_bytes(16)
unknown_target_bytes = base64.b64decode(b"""
Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg
aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq
dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg
YnkK
""")

def AES_encrypt_ECB_mode(attacker_controlled: bytes):
    blocksize = 16

    plaintext = attacker_controlled + unknown_target_bytes
    plaintext = pkcs7(plaintext, blocksize)

    cryptor = AES.new(consistent_but_unknown_key, AES.MODE_ECB)
    ciphertext = cryptor.encrypt(plaintext)

    return ciphertext
```

## Mục tiêu
Tìm được nội dung `target-bytes`.

## Solution
Làm theo từng bước được hướng dẫn là ra:

- B1: Tìm blocksize
    - tạo attacker_controlled có độ dài tăng dần
    - Khi nào mà các bytes đầu tiên bắt đầu cố định không thay đổi nữa, thì ta đã tìm được blocksize
    - python code:
        - Khi mà 2 bytes đầu không thay đổi nữa thì tìm được blocksize
    ```
    def find_blocksize():
        prev_first_two_bytes = AES_encrypt_ECB_mode(b'a')[:2]
        for i in range(2, 100):
            first_two_bytes = AES_encrypt_ECB_mode(bytes('a'*i, 'ascii'))[:2]
            if prev_first_two_bytes == first_two_bytes:
                return i - 1
            else:
                prev_first_two_bytes = first_two_bytes
    ```
    - Kết quả: blocksize = 16
    ```
    16
    ```
- B2: Kiểm tra xem có đang dùng ECB mode hay không
    - với blocksize = 16, thử nhập bytes có 32 items giống nhau. So sánh block đầu và block 2.
    - python code:
    ```
    def is_ecb(blocksize: int = 16):
        attacker_controlled = bytes('a'*32, 'ascii')
        ciphertext = AES_encrypt_ECB_mode(attacker_controlled)
        if ciphertext[0:blocksize] == ciphertext[blocksize:blocksize*2]:
            return True
        else:
            return False
    ```
    - Kết quả:
    ```
    True
    ```
- B3: 
    - Tạo attacker_controlled có block cuối có kích thước nhỏ hơn 1 bytes so với blocksize, ví dụ 'a'*15:
    - Mà ngay sau attacker_controlled thì chính là `target-bytes` => block cuối sẽ thành 'a'*15 + `ký tự đầu tiên của target-bytes`
- B4 + B5:
    - Do chỉ có một ký tự nên ta có thể dùng brute-force, thử thay tất cả các ký tự vào bytes cuối.
    - Nếu block ciphertext trùng => tìm được `ký tự đầu tiên của target-bytes`
    - python code:
    ```
    def crack():
        # b'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c'
        b_printable = string.printable

        ciphertext = AES_encrypt_ECB_mode(bytes('a'*15, 'ascii'))

        target_bytes = ''

        for c in b_printable:
            brute_force_ciphertext = AES_encrypt_ECB_mode(bytes('a'*15 + c, 'ascii'))
            if brute_force_ciphertext[:16] == ciphertext[:16]:
                target_bytes += c
                break
        
        print(target_bytes)
    ```
    - Kết quả: ký tự đầu tiên của `target-bytes` là 'R':
    ```
    R
    ```
- B6: Tương tự, tìm dần dần từng byte của `target-bytes`
    - Tìm len của `target-bytes` (đã padding): 144
    ```
    ciphertext = AES_encrypt_ECB_mode(b'')
    print(len(ciphertext))
    ```
    - Thay vì dùng attacker_controlled chỉ có độ dài 1 block như bước 5, ta dùng attacker_controlled có độ dài 144 để khi giảm dần về 0, có thể trượt dần `target-bytes` đi qua block trong khoảng [124:144]
    - Muốn tìm kí tự đầu tiên:
        - attacker_controlled: 'a'*143
        - brute_force_attacker_controlled = attacker_controlled + {prinable character}
        - so sánh ciphertext do attacker_controlled tạo ra và ciphertext do brute_force_attacker_controlled tạo ra ở vị trí [124:144]
        - => tìm được ký tự đầu tiên
    - Muốn tìm kí tự thứ hai:
        - attacker_controlled: 'a'*142
        - brute_force_attacker_controlled = attacker_controlled + `target-bytes đã tìm được` + {prinable character}
        - so sánh 2 ciphertext ở vị trí như cũ
        - => tìm được ký tự thứ hai
    - Tương tự ta sẽ tìm được hết `target-bytes`
    ```
    def crack():
        # b'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c'
        printable = string.printable

        len_target_bytes = 144
        target_bytes = ''

        for i in range(len_target_bytes):
            attacker_controlled = bytes('a'*(len_target_bytes - i - 1), 'ascii')
            ciphertext = AES_encrypt_ECB_mode(attacker_controlled)

            for c in printable:
                brute_force_attacker_controlled = attacker_controlled + bytes(target_bytes, 'ascii') + bytes(c, 'ascii')
                brute_force_ciphertext = AES_encrypt_ECB_mode(brute_force_attacker_controlled)
                if brute_force_ciphertext[128:144] == ciphertext[128:144]:
                    target_bytes += c
                    break
        return target_bytes
    ```
    Kết quả:
    ```
    Rollin' in my 5.0
    With my rag-top down so my hair can blow
    The girlies on standby waving just to say hi
    Did you stop? No, I just drove by

    ```
    Source code: [link](./challenge12.py)

## References
