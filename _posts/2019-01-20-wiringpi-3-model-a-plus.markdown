---
layout: post
title:  "wiringPi Updates for the Raspberry Pi 3 Model A+"
date:   2019-01-20 03:55:00 +0000
categories: raspberry pi wiringPi gpio
---

The [Raspberry Pi 3 Model A+](https://www.raspberrypi.org/products/raspberry-pi-3-model-a-plus/) was recently released.  As of today the [wiringPi](http://wiringpi.com/) set of tools (in particular gpio readall) doesn't completely work on this platform, because wiringPi doesn't recognise the new board type (14).

I've [forked](https://github.com/piersfinlayson/wiringPi) wiringPi and created a fix, which I've pushed [upstream](https://git.drogon.net/).  For now, if you need 3 Model A+ support you can build from my fork.

Without this fix when you run:

```
gpio readall
```

You get:

```
Oops - unable to determine board type... model: 14
```

And if you run:

```
gpio -v
```

You get:

```
gpio version: 2.46
Copyright (c) 2012-2018 Gordon Henderson
This is free software with ABSOLUTELY NO WARRANTY.
For details type: gpio -warranty

Raspberry Pi Details:
  Type: Unknown14, Revision: 00, Memory: 512MB, Maker: Sony
  * Device tree is enabled.
  *--> Raspberry Pi 3 Model A Plus Rev 1.0
  * This Raspberry Pi supports user-level GPIO access.
```