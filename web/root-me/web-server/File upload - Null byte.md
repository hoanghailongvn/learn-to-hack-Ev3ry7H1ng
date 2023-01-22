# [File upload - Null byte](https://www.root-me.org/en/Challenges/Web-Server/File-upload-Null-byte)

## Solutions

- Thử upload với một số tên file:
  - test.php: Wrong extension !
  - test.jpeg có chứa php code: fail
  - test.php.jpeg: Wrong file name !
  - test.a.jpeg: Wrong file name !
  - test.php%00.jpeg: ok
  - test.a%00.jpeg: Wrong file name !??

- upload file test.php%00.jpeg và truy cập vào file test.php sẽ lấy được flag: `YPNchi2NmTwygr2dgCCF`

## References

- <https://portswigger.net/blog/null-byte-attacks-are-alive-and-well>

## Question

- Sao tên là test.php%00.jpeg thì ok mà test.a%00.jpeg lại không được?
