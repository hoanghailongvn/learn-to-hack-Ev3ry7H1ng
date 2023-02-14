# **[set 1 - challenge 7](https://cryptopals.com/sets/1/challenges/7): AES in ECB mode**

The Base64-encoded content in this file has been encrypted via AES-128 in ECB mode under the key

"YELLOW SUBMARINE".
(case-sensitive, without the quotes; exactly 16 characters; I like "YELLOW SUBMARINE" because it's exactly 16 bytes long, and now you do too).

Decrypt it. You know the key, after all.

Easiest way: use OpenSSL::Cipher and give it AES-128-ECB as the cipher.

Do this with code.
You can obviously decrypt this using the OpenSSL command-line tool, but we're having you get ECB working in code for a reason. You'll need it a lot later on, and not just for attacking ECB.

## What is AES?

AES:

- stands for Advanced Encryption Standard
- block cipher
- key size: 128/192/256 bits
- encrypts data in blocks of 128 bits each

"AES relies on substitution-permutation network principle which means it is performed using a series of linked operations which involves replacing and shuffling of the input data." - [geeksforgeeks](https://www.geeksforgeeks.org/advanced-encryption-standard-aes/)

## What is ECB mode?

ECB:

- stands for Electronic Code Block
- Is one of the modes in block cipher:
  - The plaintext is divided into blocks of the same size (P1, P2, ..., Pn).
  - Each block is encrypted with the same key k

![ecb.png](./pictures/ecb.png)

- Advantages:
  - fast
  - multithreading can be used to speed up the computation since blocks are independent of each other
- Disadvantages:
  - With the same 2 plaintext, are encrypted to the same ciphertext, a famous example:

    ![penguin.jpg](./pictures/penguin.jpg)

## Decrypt with python

python script, required pycryptodome package:

- step 1: decode with base64
- step 2: create `cryptor` with key "YELLOW SUBMARINE" AES
- step 3: decrypt with `cryptor`

```python
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

- Block cipher modes:
  - <https://www.educba.com/block-cipher-modes-of-operation/>
- AES:
  - <https://www.geeksforgeeks.org/advanced-encryption-standard-aes/>
