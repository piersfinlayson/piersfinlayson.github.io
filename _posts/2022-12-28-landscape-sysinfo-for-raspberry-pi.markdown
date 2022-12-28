---
layout: post
title:  "landscape-sysinfo for Raspberry Pi"
date:   2022-12-28 7:00 +0000
tags:   linux raspberry pi landscape sysinfo
---

I like the output of landscape-sysinfo on my Ubuntu servers.  It looks like this:

```
  System information as of Wed Dec 28 13:51:17 UTC 2022

  System load:                      0.58935546875
  Usage of /:                       13.0% of 109.47GB
  Memory usage:                     6%
  Swap usage:                       0%
  Processes:                        126
  Users logged in:                  0
  IPv4 address for docker0:         172.17.0.1
  IPv4 address for enp2s0:          192.168.0.2
  IPv6 address for enp2s0:          <redacted>
  IPv6 address for enp2s0:          <redacted>
  IPv4 address for <redacted>:      192.168.5.2
  IPv4 address for ppp0:            <redacted>
  IPv4 address for ppp0:            <redacted>
  IPv6 address for ppp0:            <redacted>
  IPv4 address for tun0:            10.8.0.1
```

However, the landscape-common package isn't available on Raspberry Pi OS.

To build:

```
sudo apt -y install git devscripts dh-python python3-distutils-extra gawk python3-twisted python3-configobj
git clone https://github.com/CanonicalLtd/landscape-client && cd landscape-client
env DEBEMAIL="Your Name <your@email.com>" env DEBUILD_OPTS="-us -uc" make package
```

Then to install:

```
sudo apt install python3-gdbm python3-netifaces bc lshw python3-twisted python3-configobj
sudo dpkg -i ../landscape-common_22.09+git6230-0ubuntu0_arm64.deb # Or other appropriate package name
```

(Note, for some reason the package is built to the .. directory!)

Amongst other things installing this package sets up a symbolic link from /etc/update-motd.d/50-landscape-sysinfo to /usr/share/landscape/landscape-sysinfo.wrapper which provides this kind of output.

Here's sample output from a Raspberry Pi:

```
  System information as of Wed 28 Dec 13:46:31 GMT 2022

  System load:           1.04
  Usage of /:            32.2% of 234.30GB
  Memory usage:          48%
  Swap usage:            100%
  Temperature:           60.9 C
  Processes:             228
  Users logged in:       1
  IPv4 address for eth0: 192.168.0.219
  IPv6 address for eth0: <redacted>
```
