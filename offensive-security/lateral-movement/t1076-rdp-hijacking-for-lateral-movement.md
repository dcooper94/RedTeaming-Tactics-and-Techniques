---
description: >-
  This lab explores a technique that allows a SYSTEM account to move laterally
  through the network using RDP without the need for credentials.
---

# RDP Hijacking for Lateral Movement with tscon

## Execution

It is possible by design to switch from one user's desktop session to another through the Task Manager (one of the ways).

Below shows that there are two users on the system and currently the administrator session is in active:

![[rdp-admin.png]]

Let's switch to the `spotless` session - this requires knowing the user's password, which for this exercise is known, so lets enter it:

![[rdp-login.png]]

![[rdp-password.png]]

We are now reconnected to the `spotless` session:

![[rdp-spotless.png]]

Now this is where it gets interesting. It is possible to reconnect to a users session without knowing their password if you have `SYSTEM` level privileges on the system. \
Let's elevate to `SYSTEM` using psexec (privilege escalation exploits, service creation or any other technique will also do):

```
psexec -s cmd
```

![[rdp-system.png]]

Enumerate available sessions on the host with `query user`:

![[rdp-sessions.png]]

Switch to the `spotless` session without getting requested for a password by using the native windows binary `tscon.exe`that enables users to connect to other desktop sessions by specifying which session ID (`2` in this case for the `spotless` session) should be connected to which session (`console` in this case, where the active `administator` session originates from):

```csharp
cmd /k tscon 2 /dest:console
```

![[rdp-hijack-no-password.png]]

Immediately after that, we are presented with the desktop session for `spotless`:

![[rdp-spotless-with-system.png]]

## Observations

Looking at the logs, `tscon.exe` being executed as a `SYSTEM` user is something you may want to investigate further to make sure this is not a lateral movement attempt:

![[rdp-logs (1).png]]

Also, note how `event_data.LogonID` and event\_ids `4778` (logon) and `4779` (logoff) events can be used to figure out which desktop sessions got disconnected/reconnected:

![[rdp-session-disconnect.png|Administrator session disconnected]]

![[rdp-session-reconnect.png|Spotless session reconnected (hijacked)]]

Just reinforcing the above - note the usernames and logon session IDs:

![[rdp-logon-sessions.png]]

## References

[blog.gentilkiwi.com/securite/vol-de-session-rdp](http://blog.gentilkiwi.com/securite/vol-de-session-rdp)

[www.korznikov.com/2017/03/0-day-or-feature-privilege-escalation.html](http://www.korznikov.com/2017/03/0-day-or-feature-privilege-escalation.html)

[www.ultimatewindowssecurity.com/securitylog/encyclopedia/event.aspx?eventID=4778](https://www.ultimatewindowssecurity.com/securitylog/encyclopedia/event.aspx?eventID=4778)

[docs.microsoft.com/en-us/windows-server/administration/windows-commands/tscon](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/tscon)

