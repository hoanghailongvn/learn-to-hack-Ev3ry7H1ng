def pkcs7(message: bytes, length: int) -> bytes:
    diff = length - len(message)
    padding = bytes([diff]*diff)

    ret = message + padding

    return ret

if __name__ == "__main__":
    message = b"YELLOW SUBMARINE"
    print(pkcs7(message, 20))