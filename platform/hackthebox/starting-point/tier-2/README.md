# Starting Point: TIER 2

## Summary

1. [Archetype](./1.%20Archetype.md)
    - smb, mssql
    - create reverse shell
    - tools: smbclient, winPEAS, mssqlclient.py, psexec.py
2. [Oopsie](./2.%20Oopsie.md)
    - web: IDOR, access control vulnerability, file upload php
    - privilege escalation via suid
3. [Vaccine](./3.%20Vaccine.md)
    - crack zip password
    - SQLi, --os-shell, reverse shell
    - sudo -l: `vi`
    - tools: zip2john, john, sqlmap
4. [Unified](./4.%20Unified.md)
    - log4shell, mongodb, unifi network
    - tools: mongo, makepasswd
5. [Included](./5.%20Included.md)
    - web: LFI
    - tftp: use metasploit to upload file through tftp => php simple-backdoor
    - privilege escalation via lxd (alpine)
6. [Markup](./6.%20Markup.md)
    - web: default credential, XXE
    - XXE => ssh private key
    - a file scheduled by admin can be edited by normal user
