# PowerView: Active Directory Enumeration

This lab explores a couple of common cmdlets of PowerView that allows for Active Directory/Domain enumeration.

## Get-NetDomain

Get current user's domain:

![[powerview-getnetdomain.png]]

## Get-NetForest

Get information about the forest the current user's domain is in:

![[powerview-forestinfo.png]]

## Get-NetForestDomain

Get all domains of the forest the current user is in:

![[powerview-forest-domains.png]]

## Get-NetDomainController

Get info about the DC of the domain the current user belongs to:

![[powerview-getdc.png]]

## Get-NetGroupMember

Get a list of domain members that belong to a given group:

![[powerview-groups.png]]

## Get-NetLoggedon

Get users that are logged on to a given computer:

![[powerview-connected-users.png]]

## Get-NetDomainTrust

Enumerate domain trust relationships of the current user's domain:

![[powerview-domain-trusts.png]]

## Get-NetForestTrust

Enumerate forest trusts from the current domain's perspective:

![[powerview-foresttrusts.png]]

## Get-NetProcess

Get running processes for a given remote machine:

```csharp
Get-NetProcess -ComputerName dc01 -RemoteUserName offense\administrator -RemotePassword 123456 | ft
```

![[Screenshot from 2018-11-02 10-11-17.png]]

## Invoke-MapDomainTrust

Enumerate and map all domain trusts:

![[powerview-all-domain-trusts.png]]

## Invoke-ShareFinder

Enumerate shares on a given PC - could be easily combines with other scripts to enumerate all machines in the domain:

![[powerview-enumerate-shares.png]]

## Invoke-UserHunter

Find machines on a domain or users on a given machine that are logged on:

![[powerview-invoke-user-hunter.png]]

## References

[github.com/PowerShellMafia/PowerSploit](https://github.com/PowerShellMafia/PowerSploit)
