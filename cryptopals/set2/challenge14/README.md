# **[set 2 - challenge 14](https://cryptopals.com/sets/2/challenges/14): Byte-at-a-time ECB decryption (Harder)**

## Đề bài
Tương tự như bài challenge12, ta viết hàm AES-128-ECB():

AES-128-ECB(random-prefix || attacker-controlled || target-bytes, random-key)

Trong đó:
- random-prefix: consistent_but_unknown_prefix
- attacker-controlled: phần plaintext mình thích làm gì thì làm
- target-bytes: mục tiêu
- random-key: consistent_but_unknown_key

## Solution
Do random-prefix cố định nên ta có hướng giải quyết như sau:
- tìm độ dài prefix
- tìm số lượng ký tự bù vào cuối prefix để tạo thành các block đầy đủ
- tính toán vị trí block cần so sánh mới, độ dài attacker_controlled mới, rồi chỉ việc kệ cục prefix ở đó, làm như challenge12 là xong rồi

Tìm độ dài prefix:
- ta đã biết blocksize = 16, ecb mode
- với prefix cố định ở đầu, sẽ có >= 0 ciphertext block đã được cố định
- tạo attacker_controlled với độ dài 0 và 1, cho vào hàm AES, so sánh 2 ciphertext để tìm số block đã được cố định
- tăng dần độ dài attacker_controlled (gọi là i) từ 2 trở đi, so sánh ciphertext mới (len attacker_controlled = i) và ciphertext ngay trước nó (len attacker_controlled = i - 1), nếu xuất hiện thêm fixed block
    - => số lượng ký tự cần thêm vào prefix để block cuối hoàn chỉnh: i - 1
    - => độ dài prefix: số fixed block * blocksize - (i - 1)
    ```
    def find_len_prefix():
        # i == 0
        ciphertext = AES_encrypt_ECB_mode(b"")
        # Chia ciphertext thành từng block 16 bytes và cho vào list
        twoprev_ciphertext_block16 = [ciphertext[j:j+blocksize] for j in range(0, len(ciphertext), blocksize)]

        # i == 1
        ciphertext = AES_encrypt_ECB_mode(b"a")
        # Chia ciphertext thành từng block 16 bytes và cho vào list
        prev_ciphertext_block16 = [ciphertext[j:j+blocksize] for j in range(0, len(ciphertext), blocksize)]

        # Tìm số block đã được cố định
        nb_fixed_block = 0
        for i in range(len(twoprev_ciphertext_block16)):
            if twoprev_ciphertext_block16[i] == prev_ciphertext_block16[i]:
                nb_fixed_block += 1
            else:
                break

        # tăng dần độ dài attacker_controlled đến blocksize * 2 cho đến khi xuất hiện fixed block mới
        # blocksize * 2 để chắc chắn có thêm block mới cố định
        for i in range(2, blocksize * 2):
            attacker_controlled = bytes('a'*i, 'ascii')
            ciphertext = AES_encrypt_ECB_mode(attacker_controlled)
            # Chia ciphertext thành từng block 16 bytes và cho vào list
            ciphertext_block16 = [ciphertext[j:j+blocksize] for j in range(0, len(ciphertext), blocksize)]

            if ciphertext_block16[nb_fixed_block] == prev_ciphertext_block16[nb_fixed_block]:
                nb_fixed_block += 1
                return nb_fixed_block * blocksize - (i - 1)
            else:
                prev_ciphertext_block16 = ciphertext_block16
    ```

Còn lại thì như challenge12:
```
def crack():
    # b'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c'
    printable = string.printable

    len_target_bytes = 144
    target_bytes = ''

    len_prefix = fine_len_prefix()
    # độ dài string thêm vào prefix để tạo thành block hoàn chỉnh
    len_append_to_prefix = blocksize - len_prefix % blocksize
    if len_append_to_prefix == blocksize:
        len_append_to_prefix = 0
    
    # vị trí bắt đầu và kết thúc của khổi block làm nơi so sánh bruteforce
    block_start = 128 + len_prefix + len_append_to_prefix
    block_end = 144 + len_prefix + len_append_to_prefix

    for i in range(len_target_bytes):
        attacker_controlled = bytes('a'*(len_append_to_prefix + len_target_bytes - i - 1), 'ascii')
        ciphertext = AES_encrypt_ECB_mode(attacker_controlled)

        for c in printable:
            brute_force_attacker_controlled = attacker_controlled + bytes(target_bytes, 'ascii') + bytes(c, 'ascii')
            brute_force_ciphertext = AES_encrypt_ECB_mode(brute_force_attacker_controlled)
            if brute_force_ciphertext[block_start:block_end] == ciphertext[block_start:block_end]:
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

Source code: [here](./challenge14.py)
## References
