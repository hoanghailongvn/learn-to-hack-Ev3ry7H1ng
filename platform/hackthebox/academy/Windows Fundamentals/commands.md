# Commands

- Get-WmiObject:

  ```powershell
  PS C:\htb> Get-WmiObject -Class win32_OperatingSystem | select Version,BuildNumber

  Version    BuildNumber
  -------    -----------
  10.0.19041 19041
  ```

  other class: Win32_Process, Win32_Service, Win32_Bios

- xfreerdp: `xfreerdp /v:target /u:username /p:password`
- dir: `dir c:\ /a`

- tree:

  ```cmd
  tree c:\
  tree c:\ /f | more
  ```

- icacls:

  ```cmd
  icacls c:\windows
  icacls c:\users /grant joe:f
  icacls c:\users /remove joe
  ```

- smbclient: `smbclient -L IPaddressOfTarget -U htb-student`
- net share:

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
