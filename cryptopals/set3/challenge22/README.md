# **[set 3 - challenge 22](https://cryptopals.com/sets/3/challenges/22): Crack an MT19937 seed**

## insecure
Sử dụng thời gian để làm seed sẽ rất dễ bị đoán ra bằng bruteforce với số lần thử ít.

Không chỉ MT19937 mà bất kì PRNG nào sử dụng thời gian làm seed đều không an toàn. 

## Attack
Sử dụng lại class MT19937 viết trong challenge21

Viết routine() như đề bài:
```
def routine():
    sleep(randint(min_sleep_time, max_sleep_time))
    seed = int(time())
    sleep(randint(min_sleep_time, max_sleep_time))
    rng = MT19937_32(seed)

    print(f"used seed: {seed}")
    return rng.extract_number()
```
Và một hàm attack bằng bruteforce đơn giản:
```
def attack():
    first_random = routine()
    now = time()

    for i in range(max_sleep_time * 2):
        bruteforce_seed = int(now - i)
        rng = MT19937_32(bruteforce_seed)
        if (first_random == rng.extract_number()):
            print(f"found seed: {bruteforce_seed}")
            break
```
Kết quả:
```
used seed: 1656737447
found seed: 165673744
```

## References

