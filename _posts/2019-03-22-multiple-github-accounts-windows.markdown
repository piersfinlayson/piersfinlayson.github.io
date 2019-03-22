---
layout: post
title:  "Using multiple Github accounts on Windows"
date:   2019-03-22 19:02:00 +0000
categories: github windows
---

I have multiple github accounts, and frequently update each repos from these different accounts.  The default github tools config on windows stores a single logon in the Windows Credential Manager (WCM).  Attempting to access a repo which that logon doesn't have access to leads to a permissions error.

I was working around this by starting the WCM and finding and deleting the github credential whenever I needed to switche accounts.  But I've now found an easier fix [here](https://github.com/Microsoft/Git-Credential-Manager-for-Windows/issues/749), running:

```
git config --global credential.github.com.useHttpPath true
```

This puts credentials in the WCM based on the repo path, so supports different accounts.