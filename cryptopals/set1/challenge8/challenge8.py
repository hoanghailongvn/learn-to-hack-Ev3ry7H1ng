import binascii
from Crypto.Cipher import AES

if __name__ == "__main__":
    with open("8.txt", "r") as file:
        ciphertext = (file.read())
        file.close()

    # Đếm số lần xuất hiện của từng block 16 bits trong mỗi dòng lưu vào dict
    dict_cipher = {}
    for i, line in enumerate(ciphertext.split('\n')):
        b_line = binascii.unhexlify(line)

        dict_cipher[i] = {}
        for j in range(0, len(b_line), 16):
            blockk = b_line[j:j+16]
            if blockk in dict_cipher[i]:
                dict_cipher[i][blockk] += 1
            else:
                dict_cipher[i][blockk] = 1

    # In ra block nào xuất hiện nhiều hơn 1 lần
    for line in dict_cipher:
        for blockk in dict_cipher[line]:
            if dict_cipher[line][blockk] != 1:
                print(f"line: {line}")
                print(f"block: {blockk}\ntimes: {dict_cipher[line][blockk]}")