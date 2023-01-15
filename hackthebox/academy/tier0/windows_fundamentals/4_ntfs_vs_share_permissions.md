# [NTFS vs. Share Permissions](https://academy.hackthebox.com/module/49/section/1017)

Server Message Block protocol (SMB): connect shared resources like files and printers, used in large, medium and small enterprise environments.

### Share permissions

| Permission | Description |
| --- | --- |
| Full Control | all actions given by Change and Read permissions, change permissions for NTFS files and subfolders |
| Change | read, edit, delete, add files and subfolders |
| Read | view file and subfolder contents |

## Creating a Network Share

Most large enterprise environments, shares are created on a:

- Storage Area Network (SAN)
- Network Attached Storage device (NAS)
- separate partition on drives accessed via a server os like Windows Server

If we ever com across shares on a `desktop os`, it will either be:

- a small business
- beachhead system used by a pentester or malicious attacker to gather and exfiltrate data

### Creating the Folder

### Making the Folder a Share

With shared resources, both the SMB and NTFS permissions lists apply to every resourse.

Access Control List (ACL) contains access control entries (ACEs).

### using smbclient to Connect to the Share

```cmd
smbclient -L IPaddressOfTarget -U htb-student
```

### Windows Defender Firewall Considerations

The firewall has blocked access from any device that is not joined to the same `workgroup`.

`netlogon` requests are authenticated against:

- workgroup: local SAM database
- Windows Domain: centralized network-based database (Active Directory)

Like most firewalls, Windows Defender Firewall permits or denies traffic flowing `inbound` &/or `outbound`

Windows Defender Firewall Profiles:

- public
- private
- domain

Thiết lập lại inbound rule: [link](https://help.f-secure.com/product.html?business/radar/4.0/en/task_CFF0E38A5A6647B8969E6B696DA6F447-4.0-en)

### Mounting to the Share

```bash
sudo mount -t cifs -o username=htb-student,password=Academy_WinFun! //ipaddoftarget/"Company Data" /home/user/Desktop/
```

### Do you remember us sharing the C:\ drive?

The most important drive with the most critical files on a Windows system is shared via SMB at install. This means anyone with the proper access could remotely access the entire C:\ of each Windows system on a network.

## command

```powershell
C:\Users\htb-student> net share

Share name   Resource                        Remark

-------------------------------------------------------------------------------
C$           C:\                             Default share
IPC$                                         Remote IPC
ADMIN$       C:\WINDOWS                      Remote Admin
Company Data C:\Users\htb-student\Desktop\Company Data

The command completed successfully.
```

## tools

Computer Management

Event Viewer
