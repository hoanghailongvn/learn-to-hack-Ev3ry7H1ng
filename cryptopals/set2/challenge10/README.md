# **[set 2 - challenge 10](https://cryptopals.com/sets/2/challenges/10): Implement CBC mode**

## What is CBC mode?
CBC:
- Là viết tắt của Cipher block chaining
- Là một trong các mode trong block cipher như ECB
- Trong đó, giống với ECB:
    - Plain text được chia làm các blocks bằng nhau
    - Cùng được mã hóa với key k
- Khác ECB ở chỗ:
    - Mỗi block plaintext trước khi được mã hóa với key sẽ xor với ciphertext của block trước đó
    - Block đầu tiên thì sẽ xor với "fake 0th ciphertext block", gọi là `initialization vector` viết tắt là IV

<img src="pictures/CBC_e.png">

<img src="pictures/CBC_d.png">

- Advantages:
    - Không còn bị vấn đề về bảo mật như ECB mode: 2 plain text giống nhau không mã hóa thành 2 cipher text giống nhau
- Disadvantages:
    - Chậm
    - Không sử dụng được kỹ thuật đa luồng như ECB mode do phải tính toán lần lượt.

## Challenge
Như để bài, ta nên sử dụng AES decrypt với ECB mode, viết thêm code để thành CBC mode:
- Với từng block cipher text từ trái sang phải:
    - 1. decrypt như ecb mode
    - 2. xor với block cipher text trước nó (block đầu tiên thì xor với iv)

Python code:
```
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
```
Kết quả:
```
I'm back and I'm ringin' the bell 
A rockin' on the mike while the fly girls yell
In ecstasy in the back of me
Well that's my DJ Deshay cuttin' all them Z's
Hittin' hard and the girlies goin' crazy
Vanilla's on the mike, man I'm not lazy.

I'm lettin' my drug kick in
It controls my mouth and I begin
To just let it flow, let my concepts go
My posse's to the side yellin', Go Vanilla Go!

Smooth 'cause that's the way I will be
And if you don't give a damn, then
Why you starin' at me
So get off 'cause I control the stage
There's no dissin' allowed
I'm in my own phase
The girlies sa y they love me and that is ok
And I can dance better than any kid n' play

Stage 2 -- Yea the one ya' wanna listen to
It's off my head so let the beat play through
So I can funk it up and make it sound good
1-2-3 Yo -- Knock on some wood
For good luck, I like my rhymes atrocious
Supercalafragilisticexpialidocious
I'm an effect and that you can bet
I can take a fly girl and make her wet.

I'm like Samson -- Samson to Delilah
There's no denyin', You can try to hang
But you'll keep tryin' to get my style
Over and over, practice makes perfect
But not if you're a loafer.

You'll get nowhere, no place, no time, no girls
Soon -- Oh my God, homebody, you probably eat
Spaghetti with a spoon! Come on and say it!

VIP. Vanilla Ice yep, yep, I'm comin' hard like a rhino
Intoxicating so you stagger like a wino
So punks stop trying and girl stop cryin'
Vanilla Ice is sellin' and you people are buyin'
'Cause why the freaks are jockin' like Crazy Glue
Movin' and groovin' trying to sing along
All through the ghetto groovin' this here song
Now you're amazed by the VIP posse.

Steppin' so hard like a German Nazi
Startled by the bases hittin' ground
There's no trippin' on mine, I'm just gettin' down
Sparkamatic, I'm hangin' tight like a fanatic
You trapped me once and I thought that
You might have it
So step down and lend me your ear
'89 in my time! You, '90 is my year.

You're weakenin' fast, YO! and I can tell it
Your body's gettin' hot, so, so I can smell it
So don't be mad and don't be sad
'Cause the lyrics belong to ICE, You can call me Dad
You're pitchin' a fit, so step back and endure
Let the witch doctor, Ice, do the dance to cure
So come up close and don't be square
You wanna battle me -- Anytime, anywhere

You thought that I was weak, Boy, you're dead wrong
So come on, everybody and sing this song

Say -- Play that funky music Say, go white boy, go white boy go
play that funky music Go white boy, go white boy, go
Lay down and boogie and play that funky music till you die.

Play that funky music Come on, Come on, let me hear
Play that funky music white boy you say it, say it
Play that funky music A little louder now
Play that funky music, white boy Come on, Come on, Come on
Play that funky music
♦♦♦♦
```
## References
