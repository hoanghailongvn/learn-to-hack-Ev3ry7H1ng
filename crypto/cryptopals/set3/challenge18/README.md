# **[set 3 - challenge 18](https://cryptopals.com/sets/3/challenges/18): Implement CTR, the stream cipher mode**

## What is CTR mode?
<img src="pictures/ctr_e.png">

<img src="pictures/ctr_d.png">

CTR:
- Counter mode 
- Là một trong các mode của block cipher như ECB, CBC
- CTR làm cho block cipher hoạt động như stream cipher: với mỗi block sẽ tạo ra keystream khác nhau:
    - ciphertext = keystream xor plaintext (encrypt)
    - plaintext = keystream xor ciphertext (decrypt)
- không cần padding
- Advantages:
    - Mỗi block plaintext sẽ có keystream khác nhau, do đó 2 plaintext block giống nhau được encrypt thành 2 ciphertext block khác nhau.
    - Do encrypt và decrypt hoạt động ở mỗi block độc lập như ECB, có thể sử dụng đa luồng để tăng tốc độ tính toán.

## Challenge 18
keystream, trong bài này keystream được tạo bằng:
- noice: 8 bytes: để là '\x00\x00\x00\x00\x00\x00\x00\x00'
- counter biểu diễn bằng little endian 8 bytes: vd 1 -> '\x01\x00\x00\x00\x00\x00\x00\x00'
- keystream = encrypt(noice|counter)

=> python code:
- stream_xor được sửa lại so với các bài trước:
    - cũ: xor 2 bytes độ dài bằng nhau
    - mới: nhận vào 2 bytes có độ dài khác nhau, xor theo bytes ngắn hơn

    ```
    # xor 2 bytes object theo cái ngắn hơn
    def stream_xor(input1: bytes, input2: bytes) -> bytes:
        shorter = min(len(input1), len(input2))

        ret = bytes([a ^ b for a, b in zip(input1[:shorter], input2[:shorter])])
        return ret
    ```
- Hàm generate_keystream(): nhận vào nonce, counter và key, tạo ra keystream:
    - vd: nonce = '\x00' * 8
    - counter = 2
    - return encrypt(b'\x00\x00\x00\x00\x00\x00\x00\x00' + b'\x02\x00\x00\x00\x00\x00\x00\x00')
    ```
    def generate_keystream(nonce: bytes, counter: int, key: bytes):
        cryptor = AES.new(key, AES.MODE_ECB)

        return cryptor.encrypt(nonce + struct.pack("Q", counter))
    ```
- Hàm decrypt: 
    - loop từng block đến block cuối (kích thước block cuối có thể không đủ)
    - tạo keystream và xor với từng ciphertext block là ra plaintext
    ```
    def CTR_decrypt(ciphertext: bytes, key: bytes, nonce: bytes) -> bytes:
        plaintext = b""

        for counter in range(0, len(ciphertext)//blocksize + 1):
            keystream = generate_keystream(nonce, counter, key)
            plaintext += stream_xor(ciphertext[counter*blocksize : (counter+1)*blocksize], keystream)

        return plaintext
    ```

- main():
    ```
    if __name__ == "__main__":
        ciphertext = b"L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ=="
        ciphertext = base64.b64decode(ciphertext)
        key = b"YELLOW SUBMARINE"

        plaintext = CTR_decrypt(ciphertext, key, bytes(blocksize//2))
        print(plaintext)
    ```

Kết quả:
```
b"Yo, VIP Let's kick it Ice, Ice, baby Ice, Ice, baby "
```

## References