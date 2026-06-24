---
description: Defense Evasion
tags: [#defense-evasion]
---

# Installing Root Certificate

## Execution

Adding a certificate with a native windows binary:

```csharp
// attacker@victim
certutil.exe -addstore -f -user Root C:\Users\spot\Downloads\certnew.cer
```

![[certs-certutil.png]]

Checking to see the certificate got installed:

![[certs-installed.png]]

Adding the certificate with powershell:

```csharp
// attacker@victim
Import-Certificate -FilePath C:\Users\spot\Downloads\certnew.cer -CertStoreLocation Cert:\CurrentUser\Root\
```

![[certs-add-with-ps.png]]

## Observations

Advanced poweshell logging to the rescue:

![[certs-ps-logging.png]]

Commandline logging:

![[certs-logs.png]]

The CAs get installed to:

```csharp
Computer\HKEY_CURRENT_USER\Software\Microsoft\SystemCertificates\Root\Certificates\C6B22A75B0633E76C9F21A81F2EE6E991F5C94AE
```

..so it is worth monitoring registry changes there:

![[certs-registry.png]]

## References

[attack.mitre.org/wiki/Technique/T1130](https://attack.mitre.org/wiki/Technique/T1130)

