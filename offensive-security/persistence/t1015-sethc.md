---
description: Sticky keys backdoor.
---

# Sticky Keys

## Execution

Replace the originali sethc.exe with a cmd.exe and rename it. You may need to change sethc.exe owner to yourself first as TrustedIntaller may be giving you a hard time:

![[sethc-trustedinstaller.png]]

![[sethc-backdoor.png]]

Hit shift 5 times while on the logon screen to invoke the backdoor:

![[sethc-logon (1).png]]

## Observations

If you notice sethc.exe spawning well known windows processes, you may want to investigate the endpoint further:

![[sethc-enumeration.png]]
