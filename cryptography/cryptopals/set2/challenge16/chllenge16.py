from Crypto.Cipher import AES
from os import urandom

# xor 2 bytes object có độ dài bằng nhau
def stream_xor(input1: bytes, input2: bytes) -> bytes:
    if len(input1) != len(input2):
        assert("stream_xor: length not equal!")
    
    ret = bytes([a ^ b for a, b in zip(input1, input2)])
    return ret

def pkcs7(message: bytes, blocksize: int) -> bytes:
    diff = blocksize - len(message) % blocksize

    padding = bytes([diff]*diff)

    ret = message + padding
    return ret

def pkcs7_unpadding(message:bytes) -> bytes:
    pad = message[-1]
    return message[: -pad]

blocksize = 16
consistent_but_unknown_key = urandom(16)
consistent_but_unknown_iv = urandom(blocksize)

def challenge16_encrypt(attacker_controlled: bytes):
    plaintext = b"comment1=cooking%20MCs;userdata=" + attacker_controlled.replace(b'=', b'').replace(b';', b'') + b";comment2=%20like%20a%20pound%20of%20bacon"
    plaintext = pkcs7(plaintext, blocksize)

    cryptor = AES.new(consistent_but_unknown_key, AES.MODE_CBC, consistent_but_unknown_iv)
    ciphertext = cryptor.encrypt(plaintext)

    return ciphertext

def challenge16_decrypt(ciphertext: bytes):
    cryptor = AES.new(consistent_but_unknown_key, AES.MODE_CBC, consistent_but_unknown_iv)
    plaintext = cryptor.decrypt(ciphertext)
    plaintext = pkcs7_unpadding(plaintext)

    return plaintext

def is_admin(plaintext: bytes):
    return b';admin=true' in plaintext

def crack():
    attacker_controlled = bytes('a'*32, 'ascii')

    ciphertext = challenge16_encrypt(attacker_controlled)
    #Chia thành từng block 16 bytes, cho vào list
    ciphertext_block16 = [ciphertext[i:i+blocksize] for i in range(0, len(ciphertext), blocksize)]

    # plaintext3 xor ciphertext2
    temp = stream_xor(bytes('a'*16, 'ascii'), ciphertext_block16[2])
    # change ciphertext2
    fake_ciphertext_block16 = ciphertext_block16
    fake_ciphertext_block16[2] = stream_xor(temp, b".....;admin=true")

    fake_ciphertext = b''.join(fake_ciphertext_block16)
    fake_plaintext = challenge16_decrypt(fake_ciphertext)

    print(fake_plaintext)
    print(is_admin(fake_plaintext))
    
if __name__ == "__main__":
    crack()