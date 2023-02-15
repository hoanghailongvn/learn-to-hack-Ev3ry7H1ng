# [Windows Fundamentals 1](https://tryhackme.com/room/windowsfundamentals1xbx)

## I. Introduction to Windows

access the virtual machine via xfreerdp:

```shell
┌──(kali㉿kali)-[~/]
└─$ xfreerdp /v:ip /u:administrator /p:letmein123!
```

## II. Windows Editions

## III. The Desktop (GUI)

## IV. The File System

- HPFS: High Performance File System
- FAT16/FAT32: File Allocation Table
  - USB devices, MicroSD cards, etc.
- NTFS: New Technology File System
  - journaling file system
  - automatically repair the folders/files on disk using information stored in a log file
  - Supports files larger than 4GB
  - Set specific permissions on folders and files
  - Folder and file compression
  - Encryption (Encryption File System or EFS)
