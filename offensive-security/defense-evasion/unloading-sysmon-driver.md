---
description: >-
  Unload sysmon driver which causes the system to stop recording sysmon event
  logs.
---

# Unloading Sysmon Driver

## Execution

```
// attacker@victim
fltMC.exe unload SysmonDrv
```

![[sysmon-cmd.png]]

## Observations

Windows event logs suggesting `SysmonDrv` was unloaded successfully:

![[sysmon-unload-log1.png]]

As well as processes requesting special privileges:

![[sysmon-unload-log2.png]]

Note how in the last 35 minutes since the driver was unloaded, no further process creation events were recorded, although I spawned new processes during that time:

![[sysmon-last-event.png]]

Note how the system thinks that the sysmon is still running, which it is, but not doing anything useful:

![[sysmon-running.png]]

## References

[twitter.com/Moti_B/status/1019307375847723008](https://twitter.com/Moti_B/status/1019307375847723008)
