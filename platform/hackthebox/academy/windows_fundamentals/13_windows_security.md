# [Windows Security](https://academy.hackthebox.com/module/49/section/462)

Windows follows certain security principles.
These are units in the system that can be authorized or authenticated for a particular action:

- users
- computers on the network
- threads
- processes

Principles are designed to make it more difficult for attackers or malicious sofware to gain unauthorized access and exploit the system

## Security Identifier (SID)

Each of the security principals on the system has a unique security identifier (SID)

The system automatically generates SIDs.

SIDs are string values with different lengths, stored in the security database. These SIDs are added to the user's access token to identify all actions that the user is authorized to take.

A SID consists of the Identifier Authority and the Relatiev ID (RID). In an AD, SID also includes the domain SID.

```powershell
C:\Users\hoang>whoami /user

USER INFORMATION
----------------

User Name        SID
================ ============================================
seadragnol\hoang S-1-5-21-49991016-3019940889-3214804269-1001
```

SID is broken down into:
`(SID)-(revision level)-(identifier-authority)-(subauthority1)-(subauthority2)-(etc)`

| Number | Meaning | Description |
| --- | --- | --- |
| S   | SID | Identifies the string as a SID. |
| 1   | Revision Level | To date, this has never changed and has always been `1` |
| 5   | Identifier-authority | A 48-bit string that identifies the authority (the computer or network) that created the SID. |
| 21  | Subauthority1 | This is a variable number that identifies the user's relation or group described by the SID to the authority that created it. It tells us in what order this authority created the user's account |
| 49991016-3019940889-3214804269 | Subauthority2 | Tells us which computer (or domain) created the number |
| 1001 | Subauthority3 | The RID that distinguishes one account from another. Tells us whether this user is a normal user, a guest, and administrator, or part of some other group |

## Security Accounts Manager (SAM) and Access Control Entries (ACE)

Access Control Lists (ACL) contain Acess Control Entries (ACEs) that define which users, groups, or processes have access to a file or to execute a process.

## User Account Control (UAC)

## Registry

## Run and RunOnce Registry Keys

## Application Whitelisting

## AppLocker

## Local Group Policy
