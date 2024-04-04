---
layout: post
title:  "Using Circle for Pi Bare Metal Programming"
date:   2024-04-04 7:01 +0000
tags:   raspberry pi bare metal circle
---

[Circle](https://github.com/rsta2/circle) is a C/C++ bare metal programming environment for the Raspberry Pi - i.e. it provides a bunch of libraries to make bare metal programming easier.

To get it building for the Pi 4, 64-bit follow these instructions.

## Get the ARM GNU Toolchain

The latest ARM GNU toolchain is available [here](https://developer.arm.com/downloads/-/arm-gnu-toolchain-downloads).

To install the toolchain for an x86_64 host and an AArch64 bare-metal target, using version 13.2.rel1:

```
cd ~/builds
wget "https://developer.arm.com/-/media/Files/downloads/gnu/13.2.rel1/binrel/arm-gnu-toolchain-13.2.rel1-x86_64-aarch64-none-elf.tar.xz?rev=a05df3001fa34105838e6fba79ee1b23&hash=D63F63D13F01626D207019956E7122B5" -O arm-gnu-toolchain-13.2.rel1-x86_64-aarch64-none-elf.tar.xz
unxz arm-gnu-toolchain-13.2.rel1-x86_64-aarch64-none-elf.tar.xz
tar xf arm-gnu-toolchain-13.2.rel1-x86_64-aarch64-none-elf.tar
rm arm-gnu-toolchain-13.2.rel1-x86_64-aarch64-none-elf.tar
```

## Build Circle Libraries

To build for the Raspberry Pi 4, 64-bit, with a UK keyboard mapping:

```
cd ~/builds
git clone https://github.com/rsta2/circle
cd circle
PATH=$PATH:~/builds/arm-gnu-toolchain-13.2.Rel1-x86_64-aarch64-none-elf/bin ./configure -r 4 -p aarch64-none-elf- --keymap UK
PATH=$PATH:~/builds/arm-gnu-toolchain-13.2.Rel1-x86_64-aarch64-none-elf/bin ./makeall
```

The libraries are output to ```./lib```.

## Build Circle Samples

The samples are in ```./sample```.  To build a sample, go to the sample's directory and run ```make```.

For example, to build 08-usbkeyboard:

```
cd sample/08-usbkeyboard
PATH=$PATH:~/builds/arm-gnu-toolchain-13.2.Rel1-x86_64-aarch64-none-elf/bin make
```

## To run the Sample

You need an SD card with a FAT32 formatted first partition.

You can do create this via the command line, as follows, assuming you have an SD card at ```/dev/sdb``` (make sure you use the right device as this will wipe the filesystem!):

```
sudo apt install parted dosfstools
wipefs -q -all --force /dev/sdb
sudo parted -s /dev/sdb mklabel msdos
sudo parted -s /dev/sdb mkpart primary fat32 1MiB 100%
sudo mkfs -t vfat /dev/sdb1
```

Now you need the following files on the SD card:

* ```start4.elf```
* ```bcm2711-rpi-4-b.dtb```
* ```kernel8.img```

Get the first two from the [Raspberry Pi Firmware repo](https://github.com/raspberrypi/firmware).  For example:

```
wget "https://github.com/raspberrypi/firmware/raw/master/boot/start4.elf" -O /tmp/start4.elf
wget "https://github.com/raspberrypi/firmware/raw/master/boot/bcm2711-rpi-4-b.dtb" -O /tmp/bcm2711-rpi-4-b.dtb.elf
```

The last file you just built, and so it comes from the sample directory - it will be called ```kernel8-rpi4.img``` so you will need to rename.

For example to install all of these files on ```/dev/sdb1```:

```
sudo mount /dev/sdb1 /mnt
sudo cp /tmp/start4.elf /mnt
sudo cp /tmp/bcm2711-rpi-4-b.dtb /mnt
sudo cp kernel8-rpi4.img /mnt/kernel8.img
sudo umount /mnt
```

Now put the SD card in the Pi and turn it on.
