# **[set 2 - challenge 11](https://cryptopals.com/sets/2/challenges/11): An ECB/CBC detection oracle**

## Luồng hoạt động
- 1: plaintext tự chọn
- 2: thêm 5 đến 10 (ngẫu nhiên) ký tự vào đầu plaintext, thêm 5 đến 10 ký tự vào cuối plaintext
- 3: tạo key (16 bytes) ngẫu nhiên
- 4: mode ecb/cbc ngẫu nhiên
    - Nếu là cbc, tạo iv (16 bytes = blocksize) ngẫu nhiên
    - sau đó encrypt

## Oracle
Theo như đọc ở một số bài thì oracle là mình có thể chọn input tùy ý cho hàm detection.

Mà để detect được ECB như challenge8 thì ở ciphertext phải có block trùng lặp.\
=> Ta cần chọn plaintext sao cho chắc chắn ở ciphertext có block trùng. Tính toán:
- 2 block (mỗi block 16 bytes) có độ dài 32 bytes
    - => plaintext có 32 ký tự giống nhau liền nhau thì ciphertext có block trùng
- Do ở bước thêm 5 đến 10 ký tự vào đầu và cuối plaintext dẫn đến plaintext bị xê dịch
    - => Cộng thêm 10, cần tổng cộng 42 ký tự để chắc chắn có 2 block ciphertext giống nhau

=> Chọn plaintext là: "a"*42

## Code
python code:
- pkcs7:
    - do độ dài message chưa chắc chia hết cho blocksize nên cần padding
    - hàm được viết lại so với challenge9
    ```
    def pkcs7(message: bytes, blocksize: int) -> bytes:
        diff = blocksize - len(message) % blocksize

        padding = bytes([diff]*diff)

        ret = message + padding

        return ret
    ```

- append_5_10:
    ```
    def append_5_10(plaintext: bytes):
        first = randint(5, 10)
        last = randint(5, 10)
        ret = urandom(first) + plaintext + urandom(last)

        return ret
    ```
- AES_encrypt:
    - ghép từng bước lại với nhau, trong đó mode ecb/cbc được chọn ngẫu nhiên và in ra màn hình
    ```
    # AES_encrypt with 50% ecb mode and 50% cbc mode
    def AES_encrypt(plaintext: bytes):
        keysize = 16
        blocksize = 16

        plaintext = append_5_10(plaintext)
        plaintext = pkcs7(plaintext, blocksize)

        r = randint(0, 1)
        key = urandom(keysize)
        iv = urandom(blocksize)

        if r == 0: #ECB
            print("used mode: ecb")
            cryptor = AES.new(key, AES.MODE_ECB)
            ciphertext = cryptor.encrypt(plaintext)
        elif r == 1: #CBC
            print("used mode: cbc")
            cryptor = AES.new(key, AES.MODE_CBC, iv)
            ciphertext = cryptor.encrypt(plaintext)

        return ciphertext
    ```
- detect_ECB:
    - sử dụng hàm đã viết trong challenge8, sửa lại là nếu có block trùng thì return True
    ```
    def detect_ECB(ciphertext: bytes, blocksize: int = 16):
        dict_cipher = {}
        for i in range(0, len(ciphertext), blocksize):
            blockk = ciphertext[i:i+blocksize]
            if blockk in dict_cipher:
                dict_cipher[blockk] += 1
            else:
                dict_cipher[blockk] = 1

        # In ra block nào xuất hiện nhiều hơn 1 lần
        for blockk in dict_cipher:
            if dict_cipher[blockk] > 1:
                print(f"block: {blockk}\ntimes: {dict_cipher[blockk]}")
                return True
        return False
    ```
Full code: [here](./challenge11.py)

Kết quả:
```
used mode: ecb
ciphertext: b'`\xdf\x8a\x99\xd1\xbe*\xe3/\x92\x9f\xf1\xd7/n\xb4@\xe0\x04wW$\xe3 !\xc3IX\xcc\x11=\xd3@\xe0\x04wW$\xe3 !\xc3IX\xcc\x11=\xd3Pq\xbe\x85\xaa\xf4\xc4\x93\x94uM\x08?Tu\xc5'
block: b'@\xe0\x04wW$\xe3 !\xc3IX\xcc\x11=\xd3'
times: 2
detected mode: ecb
```
```
used mode: cbc
ciphertext: b"U'+\xf9\x8b6\xa6\x02\xc60\xea\x8b\xac9J\xecF\x93\xf7$\xee\xf8\xdf\xdd\x8c.\x07\xcfK\x8a5\x10\x82s_\xe9\xe4\x0e\xa6\xa7P'\x96\xf3\xf6\xf3\xeaw\x9b\xe9\xcd\xf8\xc2\xf4\x8b\r\x18cG\x8d\xbeK0\x15"
detected mode: cbc
```

## References
