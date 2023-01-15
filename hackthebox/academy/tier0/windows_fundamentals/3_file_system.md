# [File System](https://academy.hackthebox.com/module/49/section/456)

5 types of Windows file systems:

- FAT12 (no longer used on modern Windows OS)
- FAT16 (no longer used on modern Windows OS)
- FAT32
- NTFS
- exFAT

FAT32 (File Allocation Table):

- USB memory sticks, SD cards, also hard drives
- uses 32 bits of data for identifying data cluster
- pros:
  - device compatibility: computers, digital cameras, gaming consoles, smartphones, tablets, ...
  - OS cross-compatibility: from Windows 95, also supported by MacOS, Linux
- cons:
  - Only be used with files that are less than 4GB
  - No build-in data protection or file compression features
  - Must use third-party tools for file encryption

NTFS (New Technology File System):

- The default Windows file system since Windows NT 3.1
- pros:
  - Reliable and can restore the consistency of the file system in the event of a system failure or power loss.
  - Provides security by allowing us to set granular permissions on both files and folders.
  - Supports very large-sized partitions.
  - Has journaling built-in, meaning that file modifications (addition, modification, deletion) are logged.
- cons:
  - Most mobile devices do not support NTFS natively.
  - Older media devices such as TVs and digital camerars do not offer support for NTFS storage devices.

## Permissions

The NTFS file system has many basic and advanced permissions.

Some of the key permissions types:

|Permission Type| Description|
|---|---|
|Full Control| reading, writing, changing, deleting of files/folders|
|Modify| reading, writing, deleting of files/folders|
|List Folder Contents| viewing, listing folders and subfolders, executing files. Folders only inherit this permission|
|Read and Execute| viewing, listing files and subfolders, executing files. Files and folders inherit this permissions|
|Write| adding files to folders and subfolders, writing to a file|
|Read| viewing, listing folders and subfolders, viewing a files's contents|
|Traverse Folder| allows or denies the ability to move through folders to reach other files or folders|

## Integrity Control Access Control List (icacls)

NTFS permissions in Windows can be managed using:

- File Explorer GUI under the security tab
- command line: icacls utility

```cmd
C:\htb> icacls c:\windows
c:\windows NT SERVICE\TrustedInstaller:(F)
           NT SERVICE\TrustedInstaller:(CI)(IO)(F)
           NT AUTHORITY\SYSTEM:(M)
           NT AUTHORITY\SYSTEM:(OI)(CI)(IO)(F)
           BUILTIN\Administrators:(M)
           BUILTIN\Administrators:(OI)(CI)(IO)(F)
           BUILTIN\Users:(RX)
           BUILTIN\Users:(OI)(CI)(IO)(GR,GE)
           CREATOR OWNER:(OI)(CI)(IO)(F)
           APPLICATION PACKAGE AUTHORITY\ALL APPLICATION PACKAGES:(RX)
           APPLICATION PACKAGE AUTHORITY\ALL APPLICATION PACKAGES:(OI)(CI)(IO)(GR,GE)
           APPLICATION PACKAGE AUTHORITY\ALL RESTRICTED APPLICATION PACKAGES:(RX)
           APPLICATION PACKAGE AUTHORITY\ALL RESTRICTED APPLICATION PACKAGES:(OI)(CI)(IO)(GR,GE)

Successfully processed 1 files; Failed processing 0 files
```

Resource access level is list after each user in the output.

The possible inheritance settings are:

- (CI): container inherit
- (OI): object inherit
- (IO): inherit only
- (NP): do not propagate inherit
- (I): permission inherited from parent container

Basic access permissions are :

- F: full access
- D: delete access
- N: no access
- M: modify access
- RX: read and execute access
- R: read-only access
- W: write-only access

grant user control:

```cmd
icacls c:\users /grant joe:f
icacls c:\users /remove joe
```

## References

- [icacls](https://ss64.com/nt/icacls.html)
