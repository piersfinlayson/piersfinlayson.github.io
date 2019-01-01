---
layout: post
title:  "Getting more RAM on a Raspberry Pi"
date:   2019-01-02 07:59:00 +0000
categories: memory management linux rpi raspberry pi virtual memory swap docker containers
---

# Introduction

I've spent several weeks trying to compile gcc on a Raspberry Pi Zero, and, while I haven't succeeded, I have learnt a bit more about linux memory management than I knew before, so this article pulls all of that knowledge together.

# Why?

I'm creating a [common build container]({% post_url 2018-12-16-rust-compilation-for-raspberry-pi %}) which will run on all of x86\_64, ARMv6 and ARMv7 architectures, and build for all of those architectures.  Not because I _need_ to run builds on a Raspberry Pi per se, but because I like to have the same environments on all the machines I work on (so all the same utilities in place on every platform).

# Docker and Error code 137

When a docker container -  including when created via a docker build command - exits with error code 137, the system has run out of memory, and the container has been killed by the [linux Out of Memory Killer](https://www.kernel.org/doc/gorman/html/understand/understand016.html).

Sometimes, if you're lucky, rerunning the docker build will succeed.  I find that running compiling a GCC cross-compiler on a Raspberry Pi 3 will sometimes fail, and sometimes succeed - just depending on what else is going on on the device.

However, a Raspberry Pi 3 has 1GB of RAM, and a Raspberry Pi Zero only has 512 MB RAM.  I haven't yet managed to get a full compile of an ARM to x86\_64 gcc cross compiler to succeed on a Raspberry Pi Zero as part of a docker build (although I have once managed to get it to succeed within a manually created container), despite close to 100 attempts.

# Increase Swappiness

My first thought on hitting 137 was to configure the kernel to swap out more aggressively.  You can configure this using the /proc/sys/vm/swappiness setting, where the higher the more aggressive the swap - with 0 being the minimum (no swap) and 100 the max.

To set, add the following line to /etc/sysctl.conf:

```
vm.swappiness = 100
```

The reload the sysctl config with:

```
sudo sysctl --system
```

Check it's taken with:

```
cat /proc/sys/vm/swappiness
```

While this allows the build to get further it still eventually fails.

# Increase Swap Space

When increasing the swappiness didn't solve my problem I then increased the swap space.  On Raspbian this is configured by default to 100KB in size.  As well as increasing the swap space I also didn't really want to use the SD card for swapping (for fear of lots of swapping killing the SD card), so I moved swap over to an external hard disk.

Swap on Rasbian is controlled by the /etc/dphys-swapfile file.  I changed the values in this as follows:

```
CONF_SWAPFILE=/usb/swap
CONF_SWAPSIZE=4096
CONF_MAXSWAP=4096
```

Then run:

```
sudo dphys-swapfile swapoff
sudo dphys-swapfile setup # takes a while as it builds the new swapfile
sudo dphys-swapfile swapon
```

These settings give a 4096MB (4GB) swap in the /usb/ directory (which is where I mounted my external hard disk).

# Other sysctl values

When increasing swap space didn't solve the problem I played around with other kernel settings:

```
/proc/sys/vm/overcommit_memory
/proc/sys/vm/min_free_kbytes
```

The former - overcommit_memory - configures whether and how linux overcommits memory allocated to processes.  The default is 0 which implements a heuristic for when to overcommit.  It can be forced to always overcommit by changing to 1 (using the same process as changing swappiness, above).  (2 means never overcommit)

The latter - min_free_kbytes - tells the kernel to reserve and not allocate a minimum amount of RAM (usually 16MB at least on a pi) for admin and recovery actions.  Making this value bigger probably hurts rather than helps.  As the default is already pretty small there isn't really scope to improve matters by reducing.

# Using GPU RAM

The Raspberry Pi shares its RAM with the GPU as well as the CPU.  I use my Pis in headless mode, and certainly don't run X desktops on them, so don't need much RAM for the GPU.  The minimum setting is 16MB allocated to the GPU (the default being 64MB).  The can be changed by adding the following line to /boot/config.txt and rebooting:

```
gpu_mem=16
```

This sets it to the minimum.

# Tweaking Docker Memory Settings

The amount of RAM and swap available to Docker containers can be configured during the build stage using the following options:

```
--memory
--memory-swap
```

The former tells Docker to limit the amount of RAM avalable, the latter the amount of RAM and swap together (not just swap as it sounds).  I tried both set to the maximum values for my system, and neither helped.

The docker run command offers some additional options not available to docker build.  I doubt any of these would help either though, for completeness as of the time of writing the other docker run options are:

```
--memory-reservation
--memory-swappiness
--kernel-memory
--oom-kill-disable
--oom-score-adj
```

# Sample free Output

Here's an output from `free -m` during a docker build run on a Pi Zero.  This was when min_free_kbytes was set to reserve 100MB, and the 908 swap used was the maximum value I saw during the run:

```
              total        used        free      shared  buff/cache   available
Mem:            433         259         154           0          19          17
Swap:          4195         908        3287
```

And here's where I think this run fell apart (remember I had min_free_kbytes set to ~100,000 here):

```
              total        used        free      shared  buff/cache   available
Mem:            433         288          98           0          46           0
Swap:          4195          90        4104
```

# Conclusions

There's probably a few more obscure options I can tweak if I really needed to get this working - for example ensuring the Pi has as few background tasks running as possible, or even compiling a much more minimal kernel.  But I think this approach is probably on to a loser.  The next thing I'll try is building an ARMv6 container on ARMv7.

