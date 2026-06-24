---
description: Exploring ways to detect Sysmon presence on the victim system
---

# Detecting Sysmon on the Victim Host

## Processes

```csharp
// attacker@victim
PS C:\> Get-Process | Where-Object { $_.ProcessName -eq "Sysmon" }
```

![[Screenshot from 2018-10-09 17-39-28.png]]

> [!WARNING]
> Note: process name can be changed during installation

## Services

```csharp
// attacker@victim
Get-CimInstance win32_service -Filter "Description = 'System Monitor service'"
# or
Get-Service | where-object {$_.DisplayName -like "*sysm*"}
```

![[Screenshot from 2018-10-09 17-48-11.png]]

> [!WARNING]
> Note: display names and descriptions can be changed

## Windows Events

```csharp
// attacker@victim
reg query HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\WINEVT\Channels\Microsoft-Windows-Sysmon/Operational
```

![[Screenshot from 2018-10-09 17-50-47.png]]

## Filters

```
// attacker@victim
PS C:\> fltMC.exe
```

Note how even though you can change the sysmon service and driver names, the sysmon altitude is always the same - `385201`

![[Screenshot from 2018-10-09 17-51-45.png]]

## Sysmon Tools + Accepted Eula

```
// attacker@victim
ls HKCU:\Software\Sysinternals
```

![[Screenshot from 2018-10-09 17-56-33.png]]

## Sysmon -c

Once symon executable is found, the config file can be checked like so:

```
sysmon -c
```

![[Screenshot from 2018-10-09 18-43-39.png]]

## Config File on the Disk

If you are lucky enough, you may be able to find the config file itself on the disk by using native windows utility findstr:

```csharp
// attcker@victim
findstr /si '<ProcessCreate onmatch="exclude">' C:\tools\*
```

![[Screenshot from 2018-10-09 18-57-32.png]]

## Get-SysmonConfiguration

A powershell tool by @mattifestation that extracts sysmon rules from the registry:

```csharp
// attacker@victim
PS C:\tools> (Get-SysmonConfiguration).Rules
```

![[Screenshot from 2018-10-09 18-12-09.png]]

As an example, looking a bit deeper into the `ProcessCreate` rules:

```csharp
// attacker@victim
(Get-SysmonConfiguration).Rules[0].Rules
```

We can see the rules almost as they were presented in the sysmon configuration XML file:

![[Screenshot from 2018-10-09 18-13-37.png]]

A snippet from the actual sysmonconfig-export.xml file:

![[Screenshot from 2018-10-09 18-14-57.png]]

## Bypassing Sysmon

Since [Get-SysmonConfiguration](detecting-sysmon-on-the-victim-host.md#get-sysmonconfiguration) gives you the ability to see the rules sysmon is monitoring on, you can play around those.

Another way to bypass the sysmon altogether is explored here:


[unloading-sysmon-driver.md](../defense-evasion/unloading-sysmon-driver.md)


## References

[www.darkoperator.com/blog/2018/10/5/operating-offensively-against-sysmon](https://www.darkoperator.com/blog/2018/10/5/operating-offensively-against-sysmon)

[github.com/mattifestation/PSSysmonTools/blob/master/PSSysmonTools/Code/SysmonRuleParser.ps1](https://github.com/mattifestation/PSSysmonTools/blob/master/PSSysmonTools/Code/SysmonRuleParser.ps1)

[docs.microsoft.com/en-us/windows-hardware/drivers/ifs/allocated-altitudes](https://docs.microsoft.com/en-us/windows-hardware/drivers/ifs/allocated-altitudes)

[github.com/GhostPack/Seatbelt](https://github.com/GhostPack/Seatbelt)

