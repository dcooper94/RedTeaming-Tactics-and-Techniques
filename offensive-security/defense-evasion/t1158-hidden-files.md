---
description: 'Defense Evasion, Persistence'
tags: [#defense-evasion, #persistence]
---

# Hidden Files

## Execution

Hiding the file mantvydas.sdb using a native windows binary:

```csharp
// attacker@victim
PS C:\experiments> attrib.exe +h .\mantvydas.sdb
```

Note how powershell \(or cmd\) says the file does not exist, however you can type out its contents if you know the file exists:

![[attrib-nofile.png]]

Note, that `dir /a:h` \(attribute: hidden\) reveals files with a "hidden" attribute set:

![[attrib-reveal.png]]

## Observations

As usual, monitoring commandline arguments may be a good idea if you want to identify these events:

![[attrib-set.png]]

## References

[attack.mitre.org/wiki/Technique/T1158](https://attack.mitre.org/wiki/Technique/T1158)



