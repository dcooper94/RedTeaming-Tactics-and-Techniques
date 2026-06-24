---
description: Code execution with embedded HTML Form Objects
tags: [#code-execution]
---

# Phishing: Embedded HTML Forms

In this phishing lab I am just playing around with the POCs researched, coded and described by Yorick Koster in his blog post [Click me if you can, Office social engineering with embedded objects](https://securify.nl/blog/SFY20180801/click-me-if-you-can\_-office-social-engineering-with-embedded-objects.html)

## Execution

![[phishing-forms-shell.gif]]


Forms.ps1



Forms.docx


## Observations

These types of phishing documents can be identified by looking for the CLSID 5512D112-5CC6-11CF-8D67-00AA00BDCE1D in the embedded `.bin` files:

![[phishing-forms-clsid.png]]

...as well as inside the activeX1.xml file:

![[phishing-forms-xml.png]]

As usual, MS Office applications spawning cmd.exe or powershell.exe should be investigated:

![[phishing-forms-ancestry.png]]

## References

[securify.nl/blog/SFY20180801/click-me-if-you-can_-office-social-engineering-with-embedded-objects.html](https://securify.nl/blog/SFY20180801/click-me-if-you-can_-office-social-engineering-with-embedded-objects.html)
