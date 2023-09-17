---
layout: post
title:  "Setting up Windows file sharing (samba) on a Raspberry Pi NAS"
date:   2023-09-17 7:01 +0000
tags:   raspberry pi cm4 compute module nas
---

Following on from the [last post](cm4-m.2-sata) covering the hardware setup of a Raspberry Pi NAS, this post gives instructions to set up samba on the NAS, in order to access the files from a windows machine.

Install samba:

```
sudo apt update
sudo apt -y install samba samba-common-bin
```

Now configure samba using vi (or replace with your favoured editor):

```
sudo vi /etc/samba/smb.conf
```

Add to the bottom of this file:

```
[name_of_share]
path=/local/path
writeable=Yes
create mask=0777
directory mask=0777
public=no
```

Set up a Samba password for your user (replace ```<user>``` with your desired username):
```
sudo smbpasswd -a <user>
```

Enter the password, twice, as directed.

```
New SMB password:
Retype new SMB password:
Added user <user>.
```

Restart the samba service:

```
sudo service smbd restart
```

You can now access this directory from a windows machine on your local network.  From a command prompt run the following command replacing:
* ```<drive_letter>:``` with a spare drive letter (for example z:), or just use * to allocate an unused drive letter
* ```<nas>``` machine name or IP of your linux NAS
* ```<name_of_share>``` as above

```
net use <drive_letter>: \\<nas>\<name_of_share>
```

You will be prompted to enter the username and password you used above.

```
Enter the username for 'nas2': <user>
Enter the password for nas2:
The command completed successfully.
```

You can now access the contents of the share, for example:

```
dir <drive_letter>:\
```

```
 Volume in drive <drive_letter> is <name_of_share>
 Volume Serial Number is XXXX-XXXX

 Directory of drive_letter:\

17/09/2023  16:03    <DIR>          .
17/09/2023  15:28    <DIR>          ..
...
```