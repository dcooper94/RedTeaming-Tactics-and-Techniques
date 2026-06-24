---
description: Persistence
tags: [#persistence]
---

# Create Account

## Execution

```bash
// attacker@victim
net user test test123 /add /domain
```

## Observations

![[account-add.png|commandline arguments]]

There is a whole range of interesting events that could be monitored related to new account creation:

![[account-events.png]]

Details for the newly added account are logged as event `4720` :

![[account-created.png]]

## References

[attack.mitre.org/wiki/Technique/T1136](https://attack.mitre.org/wiki/Technique/T1136)



