# Alternate Data Streams

## Execution

Creating a benign text file:

```csharp
// attacker@victim
echo "this is benign" > benign.txt
Get-ChildItem
```

![[ads-benign.png]]

![](broken-reference)

Hiding an `evil.txt` file inside the `benign.txt`

```csharp
// attacker@victim
cmd '/c echo "this is evil" > benign.txt:evil.txt'
```

![[ads-evil.png]]

![](broken-reference)

Note how the evil.txt file is not visible through the explorer - that is because it is in the alternate data stream now. Opening the benign.txt shows no signs of evil.txt. However, the data from evil.txt can still be accessed as shown below in the commandline - `type benign.txt:evil.txt`:

![[ads-evil-2.png]]

Additionally, we can view the data in the notepad as well by issuing:

```csharp
// attacker@victim
notepad .\benign.txt:evil.txt
```

![[ads-evil3.png]]

## Observations

![[ads-commandline.png]]

Note that powershell can also help finding alternate data streams:

```csharp
Get-Item c:\experiment\evil.txt -Stream *
Get-Content .\benign.txt -Stream evil.txt
```

![[ads-powershell.png]]

## References

[attack.mitre.org/wiki/Technique/T1096](https://attack.mitre.org/wiki/Technique/T1096)

[docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/providers/filesystem-provider/get-item-for-filesystem?view=powershell-6](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/providers/filesystem-provider/get-item-for-filesystem?view=powershell-6)

[blog.malwarebytes.com/101/2015/07/introduction-to-alternate-data-streams](https://blog.malwarebytes.com/101/2015/07/introduction-to-alternate-data-streams/)
