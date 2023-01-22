# **[set 3 - challenge 24](https://cryptopals.com/sets/3/challenges/24): Create the MT19937 stream cipher and break it**

## Đề bài
Sử dụng MT19937 với seed 16 bit để tạo ra rng.

Sử dụng rng này để tạo ra keystream rồi xor với plaintext.

Plaintext có một phần đã biết (đề bài đề xuất sử dụng 14 ký tự 'A' liền nhau)

Tìm lại seed.

Nhận xét:
- Với seed chỉ có 16 bit, và một phần plaintext đã biết => không gian seed = 2^16 = 65536, ta có thể sử dụng brute force.

## Challenge
- Implement một số hàm cần thiết:
    - random_bytes() để tạo bytes ngẫu nhiên
    - stream_xor() để decrypt
    - generate_plaintext(): để tạo plaintext ngẫu nhiên
    ```
        def generate_plaintext() -> bytes:
        plaintext = b'A'*14
        plaintext = random_bytes(randint(0, 50)) + plaintext

        return plaintext
    ```
    - encrypt() và decrypt() có tham số là plaintext và seed cho mt19937:
    ```
    def encrypt(plaintext: bytes, mt19937_32_seed: int) -> bytes:    
        rng = MT19937_32(mt19937_32_seed)

        ciphertext = b""
        # 4 because mt19937's output is 4 bytes number
        for i in range(0, len(plaintext), 4):
            key = rng.extract_number()
            ciphertext += stream_xor(plaintext[i: i + 4], struct.pack("I", key))

        return ciphertext

    def decrypt(ciphertext: bytes, mt19937_32_seed: int) -> bytes:
        rng = MT19937_32(mt19937_32_seed)

        plaintext = b""
        # 4 because mt19937's output is 4 bytes number
        for i in range(0, len(ciphertext), 4):
            key = rng.extract_number()
            plaintext += stream_xor(ciphertext[i: i + 4], struct.pack("I", key))

        return plaintext
    ```
- Viết hàm brute force và main:
    - hàm recover_seed() tìm lại seed chỉ từ ciphertext bằng bruteforce:
    ```
    def recover_seed(ciphertext: bytes):
        for i in range(0, 2**16):
            if b"A"*14 in decrypt(ciphertext, i):
                return i
    ```
    - main:
    ```
    if __name__ == "__main__":
        # random 16 bit seed
        consistent_but_unknown_seed = randint(0, 2**16 - 1)
        print(f"used seed: {consistent_but_unknown_seed}")

        plaintext = generate_plaintext()
        ciphertext = encrypt(plaintext, consistent_but_unknown_seed)

        # tìm lại seed từ ciphertext
        start_time = time()
        recovered_seed = recover_seed(ciphertext)
        print(f"recovered seed: {recovered_seed}")
        print(f"{time() - start_time} seconds")
    ```
- Kết quả:
    - Với seed gần ở cuối của vòng lặp bruteforce: 32909, mất 28s để tìm được seed này:
    ```
    used seed: 32909
    recovered seed: 32909
    27.953020095825195 seconds
    ```


## References

