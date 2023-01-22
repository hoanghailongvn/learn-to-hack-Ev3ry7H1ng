from Crypto.Cipher import AES
import base64

if __name__ == "__main__":
    with open("7.txt", "r") as file:
        ciphertext = (file.read())
        file.close()
        
    key = b"YELLOW SUBMARINE"
    cryptor = AES.new(key, AES.MODE_ECB)

    ciphertext = base64.b64decode(ciphertext)
    plaintext = cryptor.decrypt(ciphertext).decode()

    print(plaintext)