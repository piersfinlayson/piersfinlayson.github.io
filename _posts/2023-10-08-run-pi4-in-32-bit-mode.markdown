---
layout: post
title:  "Running Raspberry Pi OS on a Pi 4 in 32-bit mode"
date:   2023-10-08 7:01 +0000
tags:   raspberry pi 4 32-bit 64-bit aarch64 armhf
---

I found myself wanting to run a Raspberry Pi 4B in 32-bit mode.  It turns out it's not enough to install the armhf Raspberry Pi OS image - as this runs the Pi with a 64-bit kernel but 32-bit packages:

```
~ $uname -a
Linux pi14 6.1.55-v8+ #1686 SMP PREEMPT Thu Oct  5 15:47:38 BST 2023 aarch64 GNU/Linux

~ $getconf LONG_BIT
32

~ $dpkg-architecture |grep "DEB_BUILD_ARCH="
DEB_BUILD_ARCH=armhf
```

The problem here is that the armhf OS image includes the 64-bit kernel ```kernel8.img``` and by default the firmware choses a 64-bit kernel for a Pi 4.

There's two obvious solutions.  The [recommended one](https://www.raspberrypi.com/documentation/computers/config_txt.html#arm_64bit) is to add this to ```/boot/config.txt```:

```
arm_64bit=0
```

This will force the firmware to chose a 32-bit kernel image.

The other option is to delete/rename ```/boot/kernel8.img``` so the firmware can't find it.
