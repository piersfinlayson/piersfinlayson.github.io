---
layout: post
title:  "Setting up Apple Filing Protocol (AFP) on a Raspberry Pi NAS"
date:   2023-09-17 7:02 +0000
tags:   raspberry pi cm4 compute module nas
---

It makes sense to follow [post about setting up Windows file sharing](samba-raspberry-pi-nas) on my NAS with a post about setting up Apple's Filing Protocol (AFP) so my shares are also easily accessible from the Apple devices in the household.

Install netatalk:

```
sudo apt update
sudo apt -y install netatalk
```

Now configure AFP support using vi (or replace with your favoured editor):

```
sudo vi /etc/netatalk/afp.conf
```

Add to the bottom of this file:

```
[name_of_share]
  path=/local/path
```

Also add a guest account for your ```<user>``` under ```[Global]```
```
[Global]
  guest account = <user>
```

Restart the netatalk service:

```
sudo service netatalk restart
```

To connect from your Apple machine, hit Cmd-K (or Finder->Go->Connect to Server) and enter:

```
afp://<nas>
```

Where ```<nas>``` is your NAS's domain name or IP address.

You'll be asked for your username and password, and you'll then be able to see and select the share you want to mount.  It'll show in the Finder's "Locations" in the sidebar.