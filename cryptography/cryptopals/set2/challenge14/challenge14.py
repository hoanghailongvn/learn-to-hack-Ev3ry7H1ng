import base64
from random import randint
from Crypto.Cipher import AES
import string
from os import urandom

def pkcs7(message: bytes, blocksize: int) -> bytes:
    diff = blocksize - len(message) % blocksize

    padding = bytes([diff]*diff)

    ret = message + padding
    return ret

blocksize = 16
consistent_but_unknown_key = urandom(16)
consistent_but_unknown_prefix = urandom(randint(0, 100))
unknown_target_bytes = base64.b64decode(b"""
Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg
aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq
dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg
YnkK
""")

def AES_encrypt_ECB_mode(attacker_controlled: bytes):
    plaintext = consistent_but_unknown_prefix + attacker_controlled + unknown_target_bytes
    plaintext = pkcs7(plaintext, blocksize)

    cryptor = AES.new(consistent_but_unknown_key, AES.MODE_ECB)
    ciphertext = cryptor.encrypt(plaintext)

    return ciphertext

def find_blocksize():
    prev_first_two_bytes = AES_encrypt_ECB_mode(b'a')[:2]
    for i in range(2, 100):
        first_two_bytes = AES_encrypt_ECB_mode(bytes('a'*i, 'ascii'))[:2]
        if prev_first_two_bytes == first_two_bytes:
            return i - 1
        else:
            prev_first_two_bytes = first_two_bytes

def is_ecb(blocksize: int = 16):
    attacker_controlled = bytes('a'*32, 'ascii')
    ciphertext = AES_encrypt_ECB_mode(attacker_controlled)
    if ciphertext[0:blocksize] == ciphertext[blocksize:blocksize*2]:
        return True
    else:
        return False

def fine_len_prefix():
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

if __name__ == "__main__":
    print(crack())
    