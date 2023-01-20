# **[set 2 - challenge 16](https://cryptopals.com/sets/2/challenges/16): CBC bitflipping attacks**

Generate a random AES key.

Combine your padding code and CBC code to write two functions.

The first function should take an arbitrary input string, prepend the string:

```text
"comment1=cooking%20MCs;userdata="
```

.. and append the string:

```text
";comment2=%20like%20a%20pound%20of%20bacon"
```

The function should quote out the ";" and "=" characters.

The function should then pad out the input to the 16-byte AES block length and encrypt it under the random AES key.

The second function should decrypt the string and look for the characters ";admin=true;" (or, equivalently, decrypt, split the string on ";", convert each resulting string into 2-tuples, and look for the "admin" tuple).

Return true or false based on whether the string exists.

If you've written the first function properly, it should not be possible to provide user input to it that will generate the string the second function is looking for. We'll have to break the crypto to do that.

Instead, modify the ciphertext (without knowledge of the AES key) to accomplish this.

You're relying on the fact that in CBC mode, a 1-bit error in a ciphertext block:

- Completely scrambles the block the error occurs in
- Produces the identical 1-bit error(/edit) in the next ciphertext block.

## Implement server-side code

- padding: pkcs7, pkcs7_unpadding
- encrypt, decrypt with cbc mode
- check is_admin

```python
from Crypto.Cipher import AES
from os import urandom

# xor 2 byte objects of the same length
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
```

## Idea

Let's take a look at the decoding process of cbc mode

![CBC_d.png](./pictures/CBC_d.png)

Với prepend text và append text có sẵn, plaintext chia thành các block sẽ như sau:

```
0: comment1=cooking
1: %20MCs;userdata=
2: [attacker.......
3: .....controlled]
4: ;comment2=%20lik
5: e%20a%20pound%20
```

Quan sát block ciphertext đến khi được decrypt thành block plaintext:

- đầu tiên sẽ đi qua decryption
- sau đó xor với block ciphertext trước nó

Ta không biết key nên không động được vô bước decryption, nhưng nếu ta có thể thay đổi block ciphertext trước đó => có thể thay đổi plaintext sau khi decrypt.

Chọn:

- attacker-controlled có độ dài 32 bytes
- đặt ";admin=true" ở block3
- thay đổi block2

```
0: comment1=cooking
1: %20MCs;userdata=
2: rác.............
3: .....;admin=true
4: ;comment2=%20lik
5: e%20a%20pound%20
```

## Solution

Tạo `attacker_controlled` = 32 ký tự 'a', các block plaintext sẽ trông như sau:

- plaintext0 = block plaintext thứ 0

```
plaintext0: b'comment1=cooking'
plaintext1: b'%20MCs;userdata='
plaintext2: b'aaaaaaaaaaaaaaaa'
plaintext3: b'aaaaaaaaaaaaaaaa'
plaintext4: b';comment2=%20lik'
plaintext5: b'e%20a%20pound%20'
plaintext6: b'of%20bacon\x06\x06\x06\x06\x06\x06'
```

Còn đây là các block ciphertext tương ứng:

- ciphertext0 = block ciphertext thứ 0

```
ciphertext0: b'\xa8\x1c\x8c\xf39\x17\xaeN\x99\xce\xfc\x1c\x9aJ\xc6l'
ciphertext1: b'\x93\xc4\xb3\xb6\x949{\x02z>\x931\xc2\xc4\xc1\xa9'
ciphertext2: b'\xc8\xdaN\xff\x89\xc3N]\xea\xf7\xd3\x93O\xd1\x8cB'
ciphertext3: b'\xcb\xd7\xd3\x0b\x97\xec96\xdb\x96\x1f\xbc\x0e\x80\xc2D'
ciphertext4: b'\x1bj\xc6V\x94.\x82k\x13\x84\xcc\xf0\xbd\xa5\x0e\x1c'
ciphertext5: b'2y\x1b\x8d`\x14\xb7C*\xb2$e\x16\xd0\x1c['
ciphertext6: b'\xe1\xf3\xfeb\xc5>\xe4\xd3\x85`\xb9v\xda\x82-\xaf'
```

ciphertext3 -> plaintext3 gồm 2 bước:

- decrypt ciphertext3 bằng aes: gọi kết quả là `after_decrypt`
- plaintext3 = `after_decrypt` xor ciphertext2

Tính nội dung cần thay vào ciphertext2:

- `after_decrypt` = plaintext3 xor ciphertext2
- thay ciphertext2 = `after_decrypt` xor ".....;admin=true"

Khi đó:

- plaintext3 = `after_decrypt` xor ciphertext2 = `after_decrypt` xor (`after_decrypt` xor ".....;admin=true") = ".....;admin=true"
=> Khi decrypt sẽ ra ";admin=true"

Python code:

```
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
```

Kết quả:

```
b'comment1=cooking%20MCs;userdata=\x97&\x06PX\x83\xc6-\xf22\xa8\xff"\xe1\xa6\xb2.....;admin=true;comment2=%20like%20a%20pound%20of%20bacon'
True
```

## References
