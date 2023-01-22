import CTR
from CTR import stream_xor
from os import urandom
import struct

## server side
consistent_but_unknown_key = urandom(16)
with open("25.txt", "r") as file:
    plaintext = bytes(file.read(), 'ascii')
    file.close()

nonce = struct.pack("Q", 0)
def edit(offset: int, newtext: bytes):
    new_plaintext = plaintext[:offset] \
                    + newtext \
                    + plaintext[offset + len(newtext):]

    return CTR.CTR(new_plaintext, consistent_but_unknown_key, nonce)

# attacker side
def recover_plaintext():
    # original ciphertext and get length of plaintext = ciphertext
    original_ciphertext = edit(0, b"")
    len_plaintext = len(edit(0, b""))

    # Cho tất cả bytes trong plaintext về \x00, lúc này ciphertext chính là keystream
    keystream = edit(0, b"\x00" * len_plaintext)

    # keystream xor original_ciphertext = original plaintext
    original_plaintext = stream_xor(keystream, original_ciphertext)

    return original_plaintext

if __name__ == "__main__":
    recovered_plaintext = recover_plaintext()
    print(recovered_plaintext == plaintext)

    



    