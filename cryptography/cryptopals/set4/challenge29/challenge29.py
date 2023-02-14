from sha1 import SHA1
from binascii import unhexlify


def sha1_mac(message: bytes):
    h = SHA1()
    h.update(b"prefix" + message)
    return unhexlify(h.hexdigest())

if __name__ == "__main__":
    recv = sha1_mac(b"comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon")
    
    h = SHA1()
    # 77 is the length of original message
    malicious_hash_value = h.length_extension_attack(recv, 77, b";admin=true")


    # check
    malicious_messsage = b'prefixcomment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x98'
    malicious_messsage = malicious_messsage + b';admin=true'
    h = SHA1()
    h.update(malicious_messsage)

    print(h.hexdigest())
    print(malicious_hash_value)
    print(h.hexdigest() == malicious_hash_value)