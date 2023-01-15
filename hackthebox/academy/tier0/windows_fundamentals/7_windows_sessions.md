# [Windows Sessions](https://academy.hackthebox.com/module/49/section/459)

## Interactive

An interactive (local logon session) is initiated by a user authenticating to a local or domain system by entering their credentials.

An interactive logon can be initiated by:

- logging directly into the system
- requesting a secondary logon session using the `runas` command via command line
- through a Remote Desktop connection

## Non-interactive

Non-interactive accounts in Windows do not require login credentials.

There are 3 types of non-interactive account:

- Local System Account (NT AUTHORITY\SYSTEM): most powerful account in Windows systems, used for OS-related tasks, more powerful than accounts in the local administrators group.
- Local Service Account (NT AUTHORITY\LocalService): less privileged version of SYSTEM account, similar privileges to a local user account.
- Network Service Account (NT AUTHORITY\NetworkService): similar to standard domain user account, similar privileges to the Local Service Account on local machine, can establish authenticated sessions for certain network services.

generally used by the Windows OS to automatically start services and applications without requiring user interaction.
