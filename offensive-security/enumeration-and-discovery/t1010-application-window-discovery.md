---
description: Discovery
---

# Application Window Discovery

Retrieving running application window titles:

```csharp
// attacker@victim
get-process | where-object {$_.mainwindowtitle -ne ""} | Select-Object mainwindowtitle
```

![[window-titles.png]]

A COM method that also includes the process path and window location coordinates:

```csharp
// attacker@victim
[activator]::CreateInstance([type]::GetTypeFromCLSID("13709620-C279-11CE-A49E-444553540000")).windows()
```

![[Annotation 2019-06-18 224603.png]]

## References

[attack.mitre.org/wiki/Technique/T1010](https://attack.mitre.org/wiki/Technique/T1010)

