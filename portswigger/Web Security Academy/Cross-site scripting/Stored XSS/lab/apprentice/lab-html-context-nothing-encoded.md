# [Lab: Stored XSS into HTML context with nothing encoded](https://portswigger.net/web-security/cross-site-scripting/stored/lab-html-context-nothing-encoded)

vào một post nào đó rồi comment với nội dung
```js
<script>alert()</script>
```

dữ liệu này sẽ được lưu vào trong db và mỗi khi người dùng khác truy cập đến nơi cần dữ liệu này thì sẽ kích hoạt xss.