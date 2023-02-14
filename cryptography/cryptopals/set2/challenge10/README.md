# **[set 2 - challenge 10](https://cryptopals.com/sets/2/challenges/10): Implement CBC mode**

CBC mode is a block cipher mode that allows us to encrypt irregularly-sized messages, despite the fact that a block cipher natively only transforms individual blocks.

In CBC mode, each ciphertext block is added to the next plaintext block before the next call to the cipher core.

The first plaintext block, which has no associated previous ciphertext block, is added to a "fake 0th ciphertext block" called the initialization vector, or IV.

Implement CBC mode by hand by taking the ECB function you wrote earlier, making it encrypt instead of decrypt (verify this by decrypting whatever you encrypt to test), and using your XOR function from the previous exercise to combine them.

[The file here](./10.txt) is intelligible (somewhat) when CBC decrypted against "YELLOW SUBMARINE" with an IV of all ASCII 0 (\x00\x00\x00 &c)

## What is CBC mode?

CBC:

- stands for Cipher block chaining
- is one of the modes in block cipher like ECB
- similar to ECB:
  - The plaintext is divided into blocks of the same size (P1, P2, ..., Pn).
  - Each block is encrypted with the same key k
- different from ECB:
  - each plaintext block before being encrypted with the key will be XORed with the ciphertext of the previous block
  - the first block is XORed with `IV`, which stands for `initialization vector`, 'fake 0th ciphertext blocks'

    ![CBC_e.png](./pictures/CBC_e.png)

    ![CBC_d.png](./pictures/CBC_d.png)

- Advantages:
  - No more security problem like ECB mode: 2 same plaintext does not encrypt into 2 same ciphertext anymore
- Disadvantages:
  - slower than ECB mode
  - Because to encrypt this block, we have the encryption result of the previous block, so we can't use multithreading like ECB.

## Solutions

as the challenge requires, we can only implement AES code with ECB mode, requiring us to write additional code to become CBC mode:

- with each ciphertext block from left to right:
  - 1. decrypt like ECB mode
  - 2. xor with previous ciphertext block (first block: XOR with iv)

Python code:

```python
import base64
from Crypto.Cipher import AES

# xor 2 bytes object have the same length
def stream_xor(input1: bytes, input2: bytes) -> bytes:
    if len(input1) != len(input2):
        assert("stream_xor: length not equal!")
    
    ret = bytes([a ^ b for a, b in zip(input1, input2)])
    return ret

# CBC mode decrypt
# With each block, decrypt by 2 step:
# - decrypt by ECB mode
# - xor with previous ciphertext block
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

result:

```text
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
