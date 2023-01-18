import base64
from Crypto.Cipher import AES

# xor 2 bytes object có độ dài bằng nhau
def stream_xor(input1: bytes, input2: bytes) -> bytes:
    if len(input1) != len(input2):
        assert("stream_xor: length not equal!")
    
    ret = bytes([a ^ b for a, b in zip(input1, input2)])
    return ret

# CBC mode decrypt
# Với mỗi block, decrypt với 2 bước:
# - decrypt với ECB mode
# - xor với block cipher text trước đó
def AES_decrypt(ciphertext: bytes, key: bytes, mode: str, iv=None) -> bytes:
    if mode == 'cbc':
        if iv is None:
            assert("AES_decrypt: iv is None")
    
    cryptor = AES.new(key, AES.MODE_ECB)

    ret = b''
    prev_cipher = iv
    for i in range(0, len(ciphertext), 16):
        blockk = ciphertext[i:i+16]
        ecb_decrypt = cryptor.decrypt(blockk)
        
        if mode == 'ecb':
            ret += ecb_decrypt
        elif mode == 'cbc':
            ret += stream_xor(ecb_decrypt, prev_cipher)
        
        prev_cipher = blockk

    return ret
        
if __name__ == "__main__":
    with open("10.txt", "r") as file:
        ciphertext = (file.read())
        file.close()

    ciphertext = base64.b64decode(ciphertext)

    key = b'YELLOW SUBMARINE'
    iv = bytes([0]*16)
    plaintext = AES_decrypt(ciphertext, b'YELLOW SUBMARINE', 'cbc', iv)
    print(plaintext.decode())