# **[set 4 - challenge 32](https://cryptopals.com/sets/4/challenges/32): Break HMAC-SHA1 with a slightly less artificial timing leak**

Giống với challenge32, nhưng giảm thời gian sleep() của mỗi lần so sánh từ 50ms xuống còn 5ms.

Khi thử với thuật toán cũ, ta có thể thấy kết tìm được sai về cuối:
```
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
80a43dcaa022c40978f0ac   <----------- sai từ đây
80a43dcaa022c40978f0ac73
```
Do thời gian thực thi mỗi lần so sánh không chính xác là 5ms, do một số yếu tố khác nên thời gian thực thi, phản hồi, sẽ xấp xỉ 5ms. Khi càng về các bytes cuối, sự xấp xỉ này sẽ cộng dồn lại với nhau khá đáng kể nên dễ bị sai.

Ta có thể bruteforce nhiều byte một lần, nhưng làm cách này sẽ tăng thời gian lên rất nhiều, ví dụ chỉ với 2 bytes một lần, thời gian sẽ là: 20 * 256 * 256 * 20 * 5 (ms) = 1.51703704 days:
- 20: tổng số vị trí cần bruteforce
- 256 * 256: 2 bytes một lần
- 20: mỗi lần bruteforce, so sánh nhiều nhất cả 20 bytes
- 5: thời gian mỗi lần so sánh

Cách hai: ta làm nổi bật 5ms lên, bằng cách không chỉ dựa vào kết quả một lần chạy, mà tổng của nhiều lần chạy với nhau, như thế độ chính xác sẽ cao hơn:
```
def attack():
    found = b""

    # brute force từng byte của signature
    for i in range(20):
        # brute force
        history = [0]*256 
        for _ in range(10):   # <---------------------------------
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
Trong đó, có thêm một vòng lặp 10 lần. Kết quả:
```
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