---
layout: post
title:  "GCC Strikes again"
date:   2024-04-04 7:02 +0000
tags:   raspberry pi bare metal gcc unaligned strict align memory alignment
---

GCC strikes [again](/2023/08/26/raspberry-pi-bare-metal-no-unaligned-access.html), generating unaligned memory access on ARM processors, causing them to trap:

[https://github.com/babbleberry/rpi4-osdev/issues/17](https://github.com/babbleberry/rpi4-osdev/issues/17#issuecomment-2036442035)

When using GCC for an aarch64 target you need the option ```-mstrict-align``` to prevent GCC from producing incompatible instructions.

For aarch32 targets you need ```-mno-unaligned-access```.