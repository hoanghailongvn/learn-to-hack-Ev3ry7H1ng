import base64
from random import randint
from Crypto.Cipher import AES
from os import urandom

ten_strings = \
"""
MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=
MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=
MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==
MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==
MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl
MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==
MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==
MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=
MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=
MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93
""".strip().split('\n')

# xor 2 bytes object có độ dài bằng nhau
def stream_xor(input1: bytes, input2: bytes) -> bytes:
    if len(input1) != len(input2):
        assert("stream_xor: length not equal!")
    
    ret = bytes([a ^ b for a, b in zip(input1, input2)])
    return ret

def pkcs7_padding(message: bytes, blocksize: int = 16) -> bytes:
    diff = blocksize - len(message) % blocksize

    padding = bytes([diff]*diff)

    ret = message + padding
    return ret

def pkcs7_padding_validate(message: bytes, blocksize: int = 16) -> bool:
    pad = message[-1]
    return message[-pad:] == bytes([pad]*pad)

def pkcs7_unpadding(message:bytes, blocksize: int = 16) -> bytes:
    pad = message[-1]
    return message[: -pad]

blocksize = 16
consistent_but_unknown_key = urandom(16)
iv = urandom(blocksize)

def challenge17_encrypt():
    plaintext = ten_strings[randint(0, 9)]
    plaintext = base64.b64decode(plaintext)
    plaintext = pkcs7_padding(plaintext, blocksize)

    cryptor = AES.new(consistent_but_unknown_key, AES.MODE_CBC, iv)
    ciphertext = cryptor.encrypt(plaintext)
    
    return ciphertext, iv

def challenge17_check_padding(ciphertext: bytes, iv: bytes) -> bool:
    cryptor = AES.new(consistent_but_unknown_key, AES.MODE_CBC, iv)
    plaintext = cryptor.decrypt(ciphertext)

    if pkcs7_padding_validate(plaintext):
        plaintext = pkcs7_unpadding(plaintext)
        return True
    else:
        return False

def crack_each_block(previous_ciphertext_block: bytes, ciphertext_block: bytes) -> bytes:
    after_decrypt = b""

    # Xử lý trường hợp 1 đầu tiên do có trường hợp đặc biệt trong đây
    i = 0
    count = 0 #only for this case, đếm số trường hợp pass padding validate
    for brute_force in range(256):
        fake_previous_ciphertext_block = bytes(16 - i - 1) + bytes([brute_force])

        if challenge17_check_padding(fake_previous_ciphertext_block + ciphertext_block, bytes(blocksize)):
            count += 1 #only for this case
            true_brute_force = brute_force
        
    if count == 1:
        after_decrypt = bytes([true_brute_force ^ (i + 1)]) + after_decrypt
    elif count > 1:
        # Nếu nhiều hơn 1 trường hợp, nghĩa là gặp trường hợp đặc biệt như đã nói trước đó
        # Thay đổi fake_previous_ciphertext_block[-2] khác đi là tìm được kết quả duy nhất
        for brute_force in range(256):
            # thay đổi fake_previous_ciphertext_block[-2] thành b"a"
            fake_previous_ciphertext_block = bytes(16 - i - 2) + b"a" + bytes([brute_force])

            if challenge17_check_padding(fake_previous_ciphertext_block + ciphertext_block, bytes(blocksize)):
                count += 1 #only for this case
                true_brute_force = brute_force

    ## các case còn lại
    for i in range(1, 16):
        for brute_force in range(256):
            # craft fake_previous_ciphertext_block
            fake_previous_ciphertext_block = bytes(16 - i - 1) + bytes([brute_force]) + stream_xor(after_decrypt, bytes([i + 1] * i))

            if challenge17_check_padding(fake_previous_ciphertext_block + ciphertext_block, bytes(blocksize)):
                true_brute_force = brute_force
                break
        
        after_decrypt = bytes([true_brute_force ^ (i + 1)]) + after_decrypt

    plaintext_block = stream_xor(after_decrypt, previous_ciphertext_block)
    
    return plaintext_block

def crack():
    ciphertext, iv = challenge17_encrypt()
    plaintext = b""

    # block 1 có previous ciphertext block là iv
    plaintext += crack_each_block(iv, ciphertext[0:blocksize])

    # từ block 2 trở đi:
    for i in range(blocksize, len(ciphertext), blocksize):
        plaintext += crack_each_block(ciphertext[i - blocksize:i], ciphertext[i:i + blocksize])

    print(plaintext)

if __name__ == "__main__":
    crack()