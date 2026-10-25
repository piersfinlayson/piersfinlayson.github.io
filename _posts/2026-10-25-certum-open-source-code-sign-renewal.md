---
layout: post
title: "Renewing a Certum Open Source Developer Code Signing Certificate"
date: 2026-10-25 07:00 +0000
tags: certum code signing open source signtool
---

Last year I bought a Certum Open Source Developer Code Signing Certificate to sign One ROM's Windows releases.  I [documented the process](/2025/10/30/certum-open-source-code-sign.html) at the time and it was a massive pain.

The certificate only lasts a year, so I had to renew.  This time I already had the smartcard and reader, but I'd reinstalled Windows since, so I had to set the software up again.

Good news - this was much less painful.  About an hour, including the Linux side.

## Buying and Verification

You buy the renewal from Certum's shop - and actually you need a new certificate, as Certum don't do renewals for open source developer certs.  This cost €25, as I already had the smartcard and reader.  You need to provide your details for verification again, from "My Account" and "Data security products".  For some reason, this year Certum decided Oswestry wasn't in Shropshire, but the West Midlands instead.

Once Certum is done, you get an email saying the verification has ended and you need to provide the key pair.  This means generating a new key pair on the smartcard.  The old key is not reused.

## Installing Smartcard Software

I installed proCertum CardManager 4.18.0 (the 64-bit .msi) from Certum's website.  This now installs Certum SignService as well, which last time I had to install separately, part way through activation.  You need to restart your PC after installing it.

Last time I installed the ACS ACR40T driver from the ACS website.  This time I didn't bother, and Windows' built-in smartcard reader driver ("Microsoft Usbccid Smartcard Reader") worked fine.

## Checking the Smartcard

Plug in the reader, start proCertum CardManager, and check it can see the card (mine is a cryptoCertum 3.6).  Under "Common Profile" you should see last year's certificate.

Do NOT reinitialise the card or reset the PIN/PUK.  You want to keep the old key until the new certificate works, and you need your existing PIN for the next step.

I checked my PIN still worked by running `certutil -scinfo` in a command prompt.  It prompted for the PIN twice, and finished with:

```
CertUtil: -SCInfo command completed successfully.
```

## Activating the Certificate

On Certum's website, go to "Data security products", choose the new certificate, and select "Activate certificate".  You then:

- choose the fields to include in the certificate
- select "Generate key pair on card"
- choose the algorithm and key length - I picked RSA 3072

When I started key generation, I got a message to download Certum SignService - even though it was already installed.  Continue with the generation.  SignService prompts for your PIN - this is the existing PIN for the card.

Once the key pair is generated, Certum issues the certificate.  From the certificate details page on the website you can install the certificate onto the card, and download it in PEM and DER format.  CardManager then listed both certificates on the card.

Check the certificate fields.  Mine came out slightly different from last year - the CN lost its comma, so Windows now displays the publisher as "Open Source Developer Piers Finlayson" rather than "Open Source Developer, Piers Finlayson".  Not a big deal, but worth knowing if you document the publisher name anywhere.

## Getting the Certificate into Windows

Last year, getting Windows to find the private key on the card was the worst bit.  This year, after installing CardManager and restarting, last year's certificate appeared in my Personal store by itself complete with the key provider information.  But the new certificate didn't appear, even after unplugging and replugging the reader.

So I did it by hand, similarly to last time.  First, add the certificate to the Personal store, using the DER file downloaded from Certum:

```
certutil -user -addstore My <CERT_FILE>.cer
```

Then tell Windows where the private key is.  You need the key container name on the card.  This lists the containers:

```
certutil -key -csp "Microsoft Smart Card Key Storage Provider"
```

I had two, one for each key.  The container name is the certificate's Subject Key Identifier with the last character dropped.

I copied the rest of the settings from the old certificate, which Windows had set up correctly.  You can see these with `certutil -v -user -store My <OLD_THUMBPRINT>`.  Note these differ from last year's post - this uses "Microsoft Smart Card Key Storage Provider" rather than "Microsoft Base Smart Card Crypto Provider":

```
[Properties]
2 = "{text}"
  _continue_ = "Container=<CONTAINER_NAME>&"
  _continue_ = "Provider=Microsoft Smart Card Key Storage Provider&"
  _continue_ = "ProviderType=0&"
  _continue_ = "Flags=0&"
  _continue_ = "KeySpec=0"
```

Then:

```
certutil -repairstore -user My <THUMBPRINT> keyinfo.inf
```

And to check it worked:

```
certutil -user -store My <THUMBPRINT>
```

This prompted for my PIN, and printed:

```
...
  Key Container = <CONTAINER_NAME>
  Provider = Microsoft Smart Card Key Storage Provider
Private key is NOT exportable
Encryption test passed
CertUtil: -store command completed successfully.
```

Note "Encryption test passed", not "Signature test passed" like last year.  That's fine.

## Signing Code

Same `signtool` command as before, with the new thumbprint:

```
signtool.exe sign /sha1 <THUMBPRINT> /fd SHA256 /td SHA256 /tr http://timestamp.digicert.com <FILE_TO_SIGN>
```

It prompted for my PIN, and signed the file:

```
Done Adding Additional Store
Successfully signed: <FILE_TO_SIGN>
```

`signtool verify /pa /v <FILE_TO_SIGN>` listed the new certificate, chained to Certum Code Signing 2021 CA and Certum Trusted Network CA 2, the same CAs as last year.

## Signing on Linux

I don't actually sign One ROM application releases on Windows.  I use [certum-code-signer](https://github.com/piersfinlayson/certum-code-signer), a small containerised web service on a Linux box with the smartcard plugged in.  Build machines send it the file and the PIN, and get the signed file back.

The card now has two keys on it, but that doesn't matter - the key is selected by its PKCS#11 ID, which is the certificate's (full) Subject Key Identifier.  So renewing just meant:

- replacing the first certificate in `signing_cert.pem` with the new one (the intermediate and root certificates haven't changed)
- setting `KEY_ID` in `.env` to the new key's ID
- rebuilding and restarting the container with `start.sh`

You can check the card has the new key, and its ID, with:

```
pkcs11-tool --module /opt/proCertumCardManager/sc30pkcs11-3.0.6.72-MS.so --list-objects
```

## The Old Key

I've left the old key and certificate on the card to expire.  There's nothing to gain from deleting them and there's a risk of deleting the wrong one.  Anything already signed with the old certificate stays valid after it expires, because the signatures are timestamped.
