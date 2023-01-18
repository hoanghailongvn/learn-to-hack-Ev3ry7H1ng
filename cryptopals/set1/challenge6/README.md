# **[set 1 - challenge 6](https://cryptopals.com/sets/1/challenges/6): Break repeating-key XOR**

## Hamming distance
Hamming distance giữa 2 string là tổng số bit khác nhau:
```
def hamming_distance(input1: bytes, input2: bytes):
    ret = 0
    
    for i in range(len(input1)):
        bin1 = f"{input1[i]:08b}"
        bin2 = f"{input2[i]:08b}"

        for j in range(8):
            if bin1[j] is not bin2[j]:
                ret += 1
    
    return ret
```
## Tìm keysize với hamming distance
Theo như đề bài gợi ý, ta sử dụng hamming distance để tìm keysize.

Ta sẽ thử với KEYSIZE lần lượt từ 2 đến khoảng 40.

Với mỗi `KEYSIZE`, tính hamming distance giữa block thứ nhất và block thứ hai có cùng `KEYSIZE` bytes của cipher text. Chia hamming distance tính được cho `KEYSIZE` để chuẩn hóa.

Với hamming distance đã chuẩn hóa nhỏ nhất => keysize.

**Giải thích**

Hamming distance giữa các ký tự trong bảng chữ cái có xác suất cao sẽ nhỏ hơn hamming distance giữa 2 số bất kỳ trong khoảng [0-255]

Với keysize đúng, hamming distance giữa các block sẽ nhỏ, và ngược lại.

## Final
Các bước cần làm:
- B1: decode ciphertext bằng base64:
    ```
    ciphertext = base64.b64decode(file.read())
    ```
- B2: Tìm keysize bằng hamming distance:
    - Hàm score_KEYSIZE (score càng nhỏ càng tốt):
        - Chia ciphertext thành các khối có kích thước `KEYSIZE`
        - Tính tổng hamming distance giữa các khối 0 và 1, 1 và 2, 2 và 3, ...
        - Chia cho `KEYSIZE` để chuẩn hóa
        - Chia cho số lượng các hamming distance đã tính
    ```
    def score_KEYSIZE(ciphertext: bytes, KEYSIZE: int):
        max_nb_block = len(ciphertext) // KEYSIZE - 1
        
        score = 0
        for i in range(max_nb_block):
            score += hamming_distance(ciphertext[KEYSIZE * i: KEYSIZE * (i + 1)], ciphertext[KEYSIZE * (i + 1): KEYSIZE * (i + 2)])
        
        score /= KEYSIZE
        score /= max_nb_block

        return score
    ```
    - Hàm guess_KEYSIZE trả về keysize có score nhỏ nhất
    ```
    def guess_KEYSIZE(ciphertext: bytes):
        min = inf
        ret = -1
        for KEYSIZE in range(2, 40):
            score = score_KEYSIZE(ciphertext, KEYSIZE)
            if min > score:
                min = score
                ret = KEYSIZE

        return ret
    ```
- B3: Khi đã có keysize, chia bài toán `crack repeating-key XOR` thành các bài toán `crack Single-byte XOR`, ví dụ:
    - plaintext: "MESSAGETEXT" được mã hóa bằng `repeating-key XOR` với key "ICE"
    - => 3 plaintext "MSEX", "EATT", "SGE" được mã hóa bằng `single-byte XOR` với key lần lượt là "I", "C", "E"

    <img src="pictures/repeat_to_single.svg">

    - Trong hàm cracking_repeat_xor, sử dụng lại hàm cracking_single_xor đã viết ở challenge3 để tìm từng ký tự trong key:
    ```
    def cracking_repeat_xor(ciphertext: bytes):
        guessed_keysize = guess_KEYSIZE(ciphertext)
        print(f"guessed keysize: {guessed_keysize}")

        key = []
        for i in range(guessed_keysize):
            temp_key, _, _ = cracking_single_xor((([ciphertext[c] for c in range(i, len(ciphertext), guessed_keysize)])))
            key.append(temp_key)

        print(bytes(key))
        print(repeating_key_xor(ciphertext, bytes(key)).decode())
    ```

Ghép tất cả lại:
```
import base64
from cmath import inf
import string
import freqAnalysis

def hamming_distance(input1: bytes, input2: bytes):
    ret = 0
    
    for i in range(len(input1)):
        bin1 = f"{input1[i]:08b}"
        bin2 = f"{input2[i]:08b}"

        for j in range(8):
            if bin1[j] is not bin2[j]:
                ret += 1
    
    return ret

def repeating_key_xor(msg: bytes, key: bytes):
    ciphertext = []

    for i, c in enumerate(msg):
        ciphertext.append(msg[i] ^ key[i % len(key)])
    
    return bytes(ciphertext)

def score_KEYSIZE(ciphertext: bytes, KEYSIZE: int):
    max_nb_block = len(ciphertext) // KEYSIZE - 1
    
    score = 0
    for i in range(max_nb_block):
        score += hamming_distance(ciphertext[KEYSIZE * i: KEYSIZE * (i + 1)], ciphertext[KEYSIZE * (i + 1): KEYSIZE * (i + 2)])
    
    score /= KEYSIZE
    score /= max_nb_block

    return score

def guess_KEYSIZE(ciphertext: bytes, size_start=2, size_end=40):
    min = inf
    ret = -1
    for KEYSIZE in range(size_start, size_end):
        score = score_KEYSIZE(ciphertext, KEYSIZE)
        if min > score:
            min = score
            ret = KEYSIZE

    return ret
        
def cracking_single_xor(b_ciphertext: bytes):
    max_score = -inf
    b_final_plaintext = b""
    final_key = -1

    for key in range(256):
        b_temp_plaintext = bytes(c ^ key for c in b_ciphertext)

        # b'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c'
        b_string_printable = bytes(string.printable, 'ascii')

        if all(p in b_string_printable for p in b_temp_plaintext):
            s = freqAnalysis.englishFreqMatchScore(b_temp_plaintext.decode('ascii'))
            if max_score < s:
                final_key = key
                max_score = s
                b_final_plaintext = b_temp_plaintext

    return final_key, max_score, b_final_plaintext

def cracking_repeat_xor(ciphertext: bytes):
    guessed_keysize = guess_KEYSIZE(ciphertext)
    print(f"guessed keysize: {guessed_keysize}")

    key = []
    for i in range(guessed_keysize):
        temp_key, _, _ = cracking_single_xor((([ciphertext[c] for c in range(i, len(ciphertext), guessed_keysize)])))
        key.append(temp_key)

    return bytes(key), repeating_key_xor(ciphertext, bytes(key))

    print(bytes(key))
    print(repeating_key_xor(ciphertext, bytes(key)).decode())


if __name__ == "__main__":
    with open("6.txt", "r") as file:
        ciphertext = base64.b64decode(file.read())
        file.close()

        key, b_plaintext = cracking_repeat_xor(ciphertext)
        print(f"Key: {key}")
        print(f"Plaintext: \n{b_plaintext.decode()}")
```
Kết quả:
```
guessed keysize: 29
Key: b'Terminator X: Bring the noise'
Plaintext: 
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
```

## References
- Hamming distance: https://nayak.io/posts/whats-so-special-about-the-hamming-distance/