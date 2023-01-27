# [Interacting with the Windows Operating System](https://academy.hackthebox.com/module/49/section/460)

## Graphical User Interface

## Remote Desktop Protocol (RDP)

port 3389

## Windows Command Line

- Command Prompt (CMD)
- PowerShell

The [Windows Command Reference](https://download.microsoft.com/download/5/8/9/58911986-D4AD-4695-BF63-F734CD4DF8F2/ws-commands.pdf) from Microsoft is a comprehensive A-Z command reference which includes an overview, usage examples, and command syntax for most Windows commands, and familiarity with it is recommended.

## CMD

The Command Prompt (cmd.exe) is used to enter and execute commands.

## PowerShell

Windows PowerShell is a command shell that was designed by Microsoft to be more geared towards system administrators. Is built on top of the .NET framework, which is used for building and running applications on Windows.

## Cmdlets

Powershell utilizes `cmdlets`, which are small single-function tools built into the shell.

There are more than 100 core cmdlets.

Cmdlets are in the from of `Verb-Noun` (ex. Get-ChildItem)

Cmdlets also take arguments or flags.

## Aliases

Many cmdlets in PowerShell also haev aliases. (ex. Set-Location is either cd or sl)

```powershell
PS C:\htb> New-Alias -Name "Show-Files" Get-ChildItem
PS C:\> Get-Alias -Name "Show-Files"

CommandType     Name                                               Version    Source
-----------     ----                                               -------    ------
Alias           Show-Files
```

## Running Scripts

The PowerShell ISE (Integrated Scripting Environment) allows users to write PowerShell scripts on the fly.

`Import-Module`
`Get-Module`

## Execution Policy

|Policy| Description|
|---|---|
|AllSigned| All scripts can run, but a trusted publisher must sign scripts and configuration files. This includes both remote and local scripts. We receive a prompt before running scripts signed by publishers that we have not yet listed as either trusted or untrusted|
|Bypass| No scripts or configuration files are blocked, and the user receives no warnings or prompts|
|Default| This sets the default execution policy, `Restricted` for Windows desktop machines and `RemoteSigned` for Windows servers|
|RemoteSigned| Scripts can run but requires a digital signature on scripts that are downloaded from the internet. Digital signatures are not required for scripts that are written locally|
|Restricted| This allows individual commands but does not allow scripts to be run. All script file types, including configuration files (.ps1xml), module script files (.psm1), and PowerShell profiles(.ps1) are blocked.|
|Undefined| No execution policy is set for the current scope. If the execution policy for ALL scopes is set to undefined, then the default execution policy of `Restricted` will be used.|
|Unrestricted| This is the default execution policy for non-Windows computers, and it cannot be changed. This policy allows for unsigned scripts to be run but warns the user before running scripts that re not from the local intranet zone.|

```powershell
PS C:\htb> Get-ExecutionPolicy -List

        Scope ExecutionPolicy
        ----- ---------------
MachinePolicy       Undefined
   UserPolicy       Undefined
      Process       Undefined
  CurrentUser       Undefined
 LocalMachine    RemoteSigned
```

A user can easily bypass the policy:

- typing the script contents directly into the PowerShell window
- downloading and invoking the script
- specifying the script as ann encoded command
- adjusting the execution policy
- setting the execution policy for the current process scope

```powershell
PS C:\htb> Set-ExecutionPolicy Bypass -Scope Process

Execution Policy Change
The execution policy helps protect you from scripts that you do not trust. Changing the execution policy might expose
you to the security risks described in the about_Execution_Policies help topic at
https:/go.microsoft.com/fwlink/?LinkID=135170. Do you want to change the execution policy?
[Y] Yes  [A] Yes to All  [N] No  [L] No to All  [S] Suspend  [?] Help (default is "N"): Y
```
