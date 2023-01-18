# **[set 4 - challenge 31](https://cryptopals.com/sets/4/challenges/31): Implement and break HMAC-SHA1 with an artificial timing leak**

# HMAC
HMAC là một loại đặc biệt của MAC, giúp chống lại tấn công length extension như đã khai thác ở challenge 29 + 30.

Pseudocode xem tại [đây](https://en.wikipedia.org/wiki/HMAC#Implementation)

python code:
```
import hashlib

def bxor(b1: bytes, b2: bytes) -> bytes: # use xor for bytes
    result = b""
    for b1, b2 in zip(b1, b2):
        print(b1, b2)
        result += bytes([b1 ^ b2])
    return result

def sha1(message: bytes) -> bytes:
    h = hashlib.sha1()
    h.update(message)
    return h.digest()

def hmac_sha1(message: bytes, key: bytes) -> bytes:
    ipad = b'\x36' * 64
    opad = b'\x5C' * 64

    if len(key) > 64:
        key = sha1(key)

    if len(key) < 64:
        key = key.ljust(64, b"\x00")

    return sha1(bxor(key, opad) + sha1(bxor(key, ipad) + message))
```

## Timing attack
[Wikipedia](https://en.wikipedia.org/wiki/Timing_attack): Every logical operation in a computer takes time to execute, and the time can differ based on the input; with precise measurements of the time for each operation, an attacker can work backwards to the input.

Ví dụ trong challenge 31 + 32, hàm insecure_compare() nhận vào 2 string, so sánh lần lượt từng byte từ trái sang phải, suy ra thời gian thực thi khi có bytes khác biệt ở đâu sẽ ngắn hơn.
## Challenge 31
Để đơn giản, ta chỉ cần viết hàm insecure_compare() là đủ rồi
```
# Server side
def random_bytes(length: int) -> bytes:
    ret = []
    for _ in range(length):
        ret.append(randint(0, 255))
    
    return bytes(ret)

consistent_but_unknown_key = random_bytes(randint(1, 20))

def insecure_compare(file: str, signature: str):
    expected = hmac_sha1(bytes(file, 'utf-8'), consistent_but_unknown_key)
    print(f"expected hash: {expected.hex()}")

    b_signature = unhexlify(signature)

    for a, b in zip(expected, b_signature):
        if a == b:
            sleep(50/1000)
            continue
        else:
            return "500"
    
    return "200"
```

Ta bruteforce từng ký tự của signature từ trái sang phải, ký tự nào làm cho hàm insecure_compare có thời gian thực thi lâu nhất thì chính là ký tự đúng:
```
def attack():
    found = b""

    # brute force từng byte của signature
    for i in range(20):
        max_time = -inf

        # brute force
        for j in range(256):
            bruteforce_signature = found[:i] + bytes([j]) + b"\x00" * (20 - i - 1)

            start_time = time()
            insecure_compare("foo", bruteforce_signature.hex())
            exe_time = time() - start_time

            if exe_time > max_time:
                found = found[:i] + bytes([j])
                max_time = exe_time
        
        print(found.hex())
```

Kết quả:
```
expected hash: 50a90948db290cc9c63991e4ffc562cfeaf98624
50
50a9
50a909
50a90948
50a90948db
50a90948db29
Traceback (most recent call last):
  File "f:\Desktop\innerDesktop\week10\set4\challenge31\challenge31.py", line 80, in <module>
    attack()
  File "f:\Desktop\innerDesktop\week10\set4\challenge31\challenge31.py", line 65, in attack
    insecure_compare("foo", bruteforce_signature.hex())
  File "f:\Desktop\innerDesktop\week10\set4\challenge31\challenge31.py", line 46, in insecure_compare
    sleep(50/1000)
KeyboardInterrupt
```
Ta có thể thấy hàm attack() đã hoạt động thành công, nên ta dừng chương trình tại đây vì thời gian chạy lâu:

Tổng thời gian chạy là: 20 * 256 * 20 * 50 = 5120000 (ms) = 1.42222222 (hours):
- 20: tổng số vị trí cần bruteforce
- 256: 1 bytes = 256 
- 20: mỗi lần bruteforce, so sánh nhiều nhất cả 20 bytes
- 50: thời gian mỗi lần so sánh

## References
Timing attack: https://en.wikipedia.org/wiki/Timing_attack
