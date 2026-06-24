---
description: Defense Evasion
tags: [#defense-evasion]
---

# Forfiles Indirect Command Execution

This technique launches an executable without a cmd.exe.

## Execution

```csharp
forfiles /p c:\windows\system32 /m notepad.exe /c calc.exe
```

![[forfiles-executed.png]]

## Observations

Defenders can monitor for process creation/commandline logs to detect this activity:

![[forfiles-ancestry.png]]

![[forfiles-cmdline.png]]

## References

[attack.mitre.org/wiki/Technique/T1202](https://attack.mitre.org/wiki/Technique/T1202)

