# **[set 1 - challenge 3](https://cryptopals.com/sets/1/challenges/3): Single-byte XOR cipher**
## XOR cipher decrypt
Nếu ta xor cipher text với key một lần nữa thì ta sẽ lấy được plaintext, đây chính là decrypt.

(A ^ B) ^ B = A ^ B ^ B = A ^ 0 = A

## has been XOR'd against a single character
Có nghĩa là mỗi kí tự trong plaintext đều đã được XOR với cùng một ký tự nào đó.

## Score method
Do keyspace bé, ta có thể sử dụng `brute-force` để thử với từng ký tự và quan sát kết quả.

Tuy nhiên, khi keyspace lớn, ta không thể quan sát kết quả bằng mắt được nữa => phải nghĩ ra công thức để tự động đánh giá `độ tốt` của mỗi kết quả.

Do mỗi ký tự trong bảng chữ cái sẽ có xác suất được sử dụng khác nhau, ta có thể sử dụng các xác suất này để đánh giá.

Đọc bài Frequency Analysis ở [đây](https://inventwithpython.com/hacking/chapter20.html), ta có được một phương pháp đánh giá đơn giản dùng python:
```
# Frequency Finder
# http://inventwithpython.com/hacking (BSD Licensed)



# frequency taken from http://en.wikipedia.org/wiki/Letter_frequency
englishLetterFreq = {'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10, 'Z': 0.07}
ETAOIN = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'



def getLetterCount(message):
    # Returns a dictionary with keys of single letters and values of the
    # count of how many times they appear in the message parameter.
    letterCount = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 'I': 0, 'J': 0, 'K': 0, 'L': 0, 'M': 0, 'N': 0, 'O': 0, 'P': 0, 'Q': 0, 'R': 0, 'S': 0, 'T': 0, 'U': 0, 'V': 0, 'W': 0, 'X': 0, 'Y': 0, 'Z': 0}

    for letter in message.upper():
        if letter in LETTERS:
            letterCount[letter] += 1

    return letterCount


def getItemAtIndexZero(x):
    return x[0]


def getFrequencyOrder(message):
    # Returns a string of the alphabet letters arranged in order of most
    # frequently occurring in the message parameter.

    # first, get a dictionary of each letter and its frequency count
    letterToFreq = getLetterCount(message)

    # second, make a dictionary of each frequency count to each letter(s)
    # with that frequency
    freqToLetter = {}
    for letter in LETTERS:
        if letterToFreq[letter] not in freqToLetter:
            freqToLetter[letterToFreq[letter]] = [letter]
        else:
            freqToLetter[letterToFreq[letter]].append(letter)

    # third, put each list of letters in reverse "ETAOIN" order, and then
    # convert it to a string
    for freq in freqToLetter:
        freqToLetter[freq].sort(key=ETAOIN.find, reverse=True)
        freqToLetter[freq] = ''.join(freqToLetter[freq])

    # fourth, convert the freqToLetter dictionary to a list of tuple
    # pairs (key, value), then sort them
    freqPairs = list(freqToLetter.items())
    freqPairs.sort(key=getItemAtIndexZero, reverse=True)

    # fifth, now that the letters are ordered by frequency, extract all
    # the letters for the final string
    freqOrder = []
    for freqPair in freqPairs:
        freqOrder.append(freqPair[1])

    return ''.join(freqOrder)


def englishFreqMatchScore(message):
    # Return the number of matches that the string in the message
    # parameter has when its letter frequency is compared to English
    # letter frequency. A "match" is how many of its six most frequent
    # and six least frequent letters is among the six most frequent and
    # six least frequent letters for English.
    freqOrder = getFrequencyOrder(message)

    matchScore = 0
    # Find how many matches for the six most common letters there are.
    for commonLetter in ETAOIN[:6]:
        if commonLetter in freqOrder[:6]:
            matchScore += 1
    # Find how many matches for the six least common letters there are.
    for uncommonLetter in ETAOIN[-6:]:
        if uncommonLetter in freqOrder[-6:]:
            matchScore += 1

    return matchScore
```
Trong hàm đánh giá đơn giản này, ta sẽ:
- Thống kê số lượng từng chữ cái trong câu, sắp xếp giảm dần
- Trong 6 chữ cái xuất hiện nhiều nhất, +1 điểm với mỗi chữ cái có trong 'ETAOIN' (6 chữ cái có tỉ lệ được dùng nhiều nhất trong tiếng anh)
- Trong 6 chữ cái xuất hiện ít nhất, +1 điểm với mỗi chữ cái có trong 'VKJXQZ' (6 chữ cái có tỉ lệ được dùng ít nhất trong tiếng anh)

## Final
Viết script python:
- xor ciphertext với từng key từ 0 - 255
- loại các xor-ed text mà có non printable character
- sử dụng hàm python ở trên để lấy điểm

```
from binascii import unhexlify
from cmath import inf
import string
import freqAnalysis

def crack(b_ciphertext: bytes):
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

if __name__ == "__main__":
    b_ciphertext = unhexlify(b'1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736')
    key, score, b_plaintext = crack(b_ciphertext)
    print(f"key: {key}\nscore: {score}\nplaintext: {b_plaintext}")
```

Kết quả:
```
key: 88
score: 5
plaintext: b"Cooking MC's like a pound of bacon"
```

## References
- Frequency Analysis: https://inventwithpython.com/hacking/chapter20.html
