# **[set 4 - challenge 32](https://cryptopals.com/sets/4/challenges/32): Break HMAC-SHA1 with a slightly less artificial timing leak**

Reduce the sleep in your "insecure_compare" until your previous solution breaks. (Try 5ms to start.)

Now break it again.

## Analysis

try using the attack function written in challenge 31:

```text
expected hash: 80a43dcaa022c40978f0ec3314136d87cee30c04
80
80a4
80a43d
80a43dca
80a43dcaa0
80a43dcaa022
80a43dcaa022c4
80a43dcaa022c409
80a43dcaa022c40978
80a43dcaa022c40978f0
80a43dcaa022c40978f0ac   <----------- wrong
80a43dcaa022c40978f0ac73
```

Since the execution time for each comparison is not exactly 5ms, due to some other factors the execution time, the response will be approximately 5ms. When these approximations are put together, they will be quite significant and prone to error.

we need to find some way to make the delay as significant as challenge 31

Solution 1:

bruteforce two bytes at a time

- time difference between true and false comparison: 5ms -> 10ms
- total time to attack: 20 *256* 256 *20* 5 (ms) = 1.51703704 days

=> too slow and can still fail, 5ms -> 10ms is not enough

Solution 2: repeat 10 times and sumup total delay

- 5ms -> 50ms
- total time to attack: same as challenge 31

this solution is ok (i think)

```python
def attack():
    found = b""

    # brute force each byte of signature
    for i in range(20):
        # brute force
        history = [0]*256 
        for _ in range(10):   # <--------------------------------- difference here
            for j in range(256):
                bruteforce_signature = found[:i] + bytes([j]) + b"\x00" * (20 - i - 1)

                start_time = time()
                insecure_compare("foo", bruteforce_signature.hex())
                exe_time = time() - start_time

                history[j] += exe_time

        max_time = max(history)
        max_index = history.index(max_time)
        found += bytes([max_index])
        
        print(found.hex())
```

result:

```text
expected hash: fb6edb9c1f22c37310e348da16ec42661cb58d68
fb
fb6e
fb6edb
fb6edb9c
fb6edb9c1f
fb6edb9c1f22
fb6edb9c1f22c3
fb6edb9c1f22c373
fb6edb9c1f22c37310
...
```

## References
