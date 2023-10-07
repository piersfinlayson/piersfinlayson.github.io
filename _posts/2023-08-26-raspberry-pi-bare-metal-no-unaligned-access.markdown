---
layout: post
title:  "Raspberry Pi Bare Metal Programming and -mno-unaligned-access"
date:   2023-08-26 7:00 +0000
tags:   bare metal raspberry pi gcc no-unaligned-access pi1541 c64
---

## TLDR

I spent a few days getting to the bottom of an incompatibility between a bare metal Raspberry Pi project, and more recent GCC versions.

The TLDR is that
* when building bare metal for Raspberry Pi 2 and 3
* using the  GCC architecture flags for the specific processors
* using recent GCC versions (likely to be 10 onwards)

requires the architecture flag -mno-unaligned-access to be set as well.

For example for a Raspberry Pi 3B+ aarch32 build this is a sensible set of GCC -m flags:

```
-march=armv8-a+crc -mtune=cortex-a53 -mfpu=crypto-neon-fp-armv8 -mfloat-abi=hard -marm -mno-unaligned-access
```

And for the Raspberry Pi 2B:

```
-march=armv7-a -mtune=cortex-a7 -mfpu=neon-vfpv4 -mfloat-abi=hard -marm -mno-unaligned-access
```

Edit 7 Oct 23: - the same ```-mno-unaligned-access``` must be added for all other boards, including the zero.

## Detail

Specifically I was initially trying to build [Pi1541](https://github.com/pi1541/Pi1541), with the gcc-arm-none-eabi toolchain provided with Ubuntu 22.04, which is currently based on GCC version 10.3.  This produced a Pi1541 image that failed to boot on a Raspberry Pi 3B+ (showing only the GPU's coloured splashed screen).

I experimented with different versions of the [toolchain](https://developer.arm.com/Tools%20and%20Software/GNU%20Toolchain) from [ARM's developer site](https://developer.arm.com).  An image built with 9.2 and earlier toolchains (including 5.4 which the project maintainer was using) booted fine, whereas an image built with 10.2 onwards would fail to boot.  ARM's developer site doesn't seem to make available GCC v9.3-9.5 or v10.0-10.1, hence I didn't test with those (my life is too short to build GCC toolchains unless I have to).

To diagnose where the failure was occuring I connected to the Pi's UART port and enabled serial logging in the Pi1541 project.  However, initially this didn't help, as the failure was so early in the kernel image execution that the UART initialization code wasn't being run.  I ended up initializing the UART before the __libc_init_array() call, which I _think_ sets up the global variables.  And it was in this global variable initialization code that I found unaligned memory access happening, leading to the processor throwing a Data Abort exception.  Helpfully Pi1541 already had code to catch and log on processor exceptions.

I saw a number of different unaligned data accesses in the code (as often when I made a code change I got a different set of assembler from the optimizer).  Here's an example:

```
 strh    r3, [r4, #55]
```

STRH is an instruction to load a half-word (2 byte value) into a register.  As r4 was pointing to a 8-byte aligned value at the time of the execution the CPU was throwing an exception, because this instruction tells the CPU to load a half-word into a 55 bytes positive offset from the address in register r4.

I was a bit confused as to why GCC would generate code which causes unaligned memory access, despite having the correct architecture settings from the processors.  These were:

```
# Pi 3
-march=armv8-a+crc -mtune=cortex-a53 -mfpu=crypto-neon-fp-armv8 -mfloat-abi=hard -marm
# Pi 2
-march=armv7-a -mtune=cortex-a7 -mfpu=neon-vfpv4 -mfloat-abi=hard -marm
# Older variants
-march=armv6zk -mtune=arm1176jzf-s -mfpu=vfp -mfloat-abi=hard
```

Finally I stumbled across the GCC documentation for the [-mno-unaligned-access](https://gcc.gnu.org/onlinedocs/gcc/ARM-Options.html#index-mno-unaligned-access) setting:

>[Disables] reading and writing of 16- and 32- bit values from addresses that are not 16- or 32- bit aligned. By default unaligned access is disabled for all pre-ARMv6, all ARMv6-M and for ARMv8-M Baseline architectures, and enabled for all other architectures. If unaligned access is not enabled then words in packed data structures are accessed a byte at a time.

The Raspberry Pi 3 uses a Cortex ARMv8-A (not M) processor (the Cortex A53) and the Pi 2 an ARMv7-A (the Cortex-A7).

Aside, I am amused as I write this that the [Raspberry Pi documentation of the BCM2836](https://www.raspberrypi.com/documentation/computers/processors.html) used in the Pi 2 says this (my emphasis in italics):

>The Broadcom chip used in the Raspberry Pi 2 Model B. The underlying architecture in BCM2836 is _identical_ to BCM2835. The _only_ significant difference is the removal of the ARM1176JZF-S processor and replacement with a quad-core Cortex-A7 cluster.

Given the GCC documentation maybe it's not unreasonable that GCC doesn't automatically enforce aligned access for the ARMv7-A and ARMv8-A - it doesn't say it will so it's working as designed.  But why is is designed this way?

I read the [Cortex-A53 technical reference](https://developer.arm.com/documentation/ddi0500/latest/) and the [Armv8-A memory model](https://developer.arm.com/-/media/Arm%20Developer%20Community/PDF/Learn%20the%20Architecture/Armv8-A%20memory%20model%20guide.pdf?revision=58b1dd0a-3800-4218-b21a-f95a0332034c) to see if I could understand why unaligned memory access on this processor would cause a problem.

I'm still not entirely sure why, but have found some possible reasons:

1. When operating in aarch32 mode (which Pi1541 uses), I read a statement somewhere (which I can no longer find) the processor operates in a mode consistent with previous versions of the architecture.  Previous versions (at least v6 and earlier) require aligned memory access.

2. It is possible to run an ARMv8-A processor in a mode that will catch unaligned memory access.  This is configured via the SCTLR and SCTLR.ELx registers, using the A bit - Alignment check enable.  However, the documentations says this is disabled on reset, and Pi1541 doesn't appear to set any of these registers.  I haven't checked the values when executing.

3. Aligned memory access is required when accessing "Device" memory.  I don't believe this is relevant as I think this refers to memory associated with peripherals.

I suspect the first reason above it the cause of the problem.  Either because the Pi1541 is being built as an aarch32 image, meaning the CPU is running in aarch32 mode, or as a result of the SD card image that I have put together to boot the Pi only including the 32-bit versions of the various Pi firmware files.

## Pi1541

This is a great project which, combined with an appropriate Pi Hat, allows you to turn a Pi into a Commodore 1541 (or 1851) disk drive, obviating the need for a real device.

In order to create a complete bootable SD card image for a Pi1541 you also need:

* The [Pi firmware files](https://github.com/raspberrypi/firmware)
* Some other pieces compiled using a 6502 compiler such as [acme](https://github.com/meonwax/acme)

I've created a Docker-based script to automatically create the SD card, here: [pi1541-build](https://github.com/piersfinlayson/pi1541-build).