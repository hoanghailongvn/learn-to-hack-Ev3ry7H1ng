def pkcs7_padding_validate(input: bytes) -> bool:
    pad = input[-1]
    return input[-pad:] == bytes([pad]*pad)

if __name__ == "__main__":
    print(pkcs7_padding_validate(b"asdf\x04\x04\x04\x04"))
    print(pkcs7_padding_validate(b"asdf\x04\x04\x04\x05"))
    