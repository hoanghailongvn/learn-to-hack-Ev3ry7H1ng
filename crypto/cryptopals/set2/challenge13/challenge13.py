from Crypto.Cipher import AES
from os import urandom

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

def cookie2dict(s: str) -> dict:
    return dict(map(lambda x: x.split('='), s.strip('&').split('&')))

def dict2cookie(d: dict) -> str:
    return '&'.join(map('='.join, d.items()))

# 1. produce dict
# 2. from dict encode to cookie
def profile_for(email: str):
    return dict2cookie({
        'email': email.replace('&', '').replace('=', ''),
        'uid': str(10),
        'role': 'user'
    })

def AES_encrypt(encoded_cookie):
    cryptor = AES.new(consistent_but_unknown_key, AES.MODE_ECB)
    ciphertext = cryptor.encrypt(pkcs7(encoded_cookie, blocksize))
    return ciphertext

def AES_decrypt_and_parse(encrypted_cookie: bytes) -> dict:
    cryptor = AES.new(consistent_but_unknown_key, AES.MODE_ECB)
    encoded_cookie = pkcs7_unpadding(cryptor.decrypt(encrypted_cookie))

    return cookie2dict(encoded_cookie.decode())

def recv_encrypted_cookie_for(email: str) -> bytes:
    cookie = profile_for(email)
    encrypted_cookie = AES_encrypt(bytes(cookie, 'ascii'))
    return encrypted_cookie

def crack():
    email = 'aaaaaaaaaa' + 'admin' + '\x0b'*0x0b + 'aaa'

    encrypted_cookie = recv_encrypted_cookie_for(email)
    # Chia encrypted_cookie thành các block 16 bytes rồi cho vào list
    encrypted_cookie_block16 = [encrypted_cookie[i:i+blocksize] for i in range(0, len(encrypted_cookie), blocksize)]

    fake_encrypted_cookie = encrypted_cookie_block16[0] + encrypted_cookie_block16[3] + \
                            encrypted_cookie_block16[2] + encrypted_cookie_block16[1]

    profile = AES_decrypt_and_parse(fake_encrypted_cookie)
    print(profile)

if __name__ == "__main__":
    crack()
