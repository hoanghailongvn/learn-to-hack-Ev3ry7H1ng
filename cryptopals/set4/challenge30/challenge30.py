from md4 import MD4
from binascii import unhexlify


def md4_mac(message: bytes):
    return unhexlify(MD4(b"prefix" + message).hexdigest())

if __name__ == "__main__":
    recv = md4_mac(b"comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon")
    
    h = MD4()
    # 77 is the length of original message
    malicious_hash_value = h.length_extension_attack(recv, 77, b";admin=true")


    # check
    malicious_messsage = b'prefixcomment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x98\x02\x00\x00\x00\x00\x00\x00'
    malicious_messsage = malicious_messsage + b';admin=true'
    h = MD4(malicious_messsage)

    print(malicious_messsage)
    print(h.hexdigest())
    print(malicious_hash_value)
    print(h.hexdigest() == malicious_hash_value)