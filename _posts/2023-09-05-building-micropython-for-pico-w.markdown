---
layout: post
title:  "Building MicroPython for the Raspberry Pi Pico W"
date:   2023-09-05 7:00 +0000
tags:   raspberry pi pico bare metal gcc arm python MicroPython
---

Instructions for building MicroPython from source from a newly installed Raspberry Pi (with a 64-bit OS).  The Raspberry Pi official documentation for doing this is [here](https://datasheets.raspberrypi.com/pico/raspberry-pi-pico-python-sdk.pdf).

## ARM GNU Toolchain

Get the ARM GNU bare metal toolchain.  These instructions get the version from ARM's developer website, rather than whatever version your linux distribution has.  Version 12.3.rel1 was the most up to date version at the time of writing, but you can check out the latest from [ARM's developer website](https://developer.arm.com/downloads/-/arm-gnu-toolchain-downloads).
* To build on a Raspberry Pi 64-bit for a Pico you need the "AArch64 linux hosted cross toolchain", "AArch32 bare-metal target" (arm-none-eabi).
  * Run the commands shown below.
* If you're building on an x86_64 machine, you'll need "x86_64 Linux hosted cross toolchains", for arm-none-eabi.  Substitute these links and filenames on the two wget commands and below:
  * [arm-gnu-toolchain-12.3.rel1-x86_64-arm-none-eabi.tar.xz](https://developer.arm.com/-/media/Files/downloads/gnu/12.3.rel1/binrel/arm-gnu-toolchain-12.3.rel1-x86_64-arm-none-eabi.tar.xz?rev=dccb66bb394240a98b87f0f24e70e87d&hash=97EE9A221DB712D24F9FB455395AF0D487F61BFE)
  * [arm-gnu-toolchain-12.3.rel1-x86_64-arm-none-eabi.tar.xz.sha256asc](https://developer.arm.com/-/media/Files/downloads/gnu/12.3.rel1/binrel/arm-gnu-toolchain-12.3.rel1-x86_64-arm-none-eabi.tar.xz.sha256asc?rev=8c830bbb97954110bbf78af753a2f3b7&hash=4C9B58EC52ABC1122267D7461D13A0321B721BB4)
* If you're building a Pi with a 32-bit OS, you'll need to install the GNU toolchain from your distribution, as ARM doesn't provide one directly.  On Raspberry Pi OS you need to install
  * gcc-arm-none-eabi
  * libnewlib-arm-none-eabi

```
wget "https://developer.arm.com/-/media/Files/downloads/gnu/12.3.rel1/binrel/arm-gnu-toolchain-12.3.rel1-aarch64-arm-none-eabi.tar.xz?rev=420215e7c8d14d90b5227eb5486d8c75&hash=147F00293D4A8065E7222F29A1BCD05BFE94DF88" -O /tmp/arm-gnu-toolchain-12.3.rel1-aarch64-arm-none-eabi.tar.xz
wget "https://developer.arm.com/-/media/Files/downloads/gnu/12.3.rel1/binrel/arm-gnu-toolchain-12.3.rel1-aarch64-arm-none-eabi.tar.xz.sha256asc?rev=bc473fd4772442ac9685dd58bd883820&hash=B47F2D832A2F3B427FF1690B4C9066CA7FC88FAF" -O /tmp/arm-gnu-toolchain-12.3.rel1-aarch64-arm-none-eabi.tar.xz.sha256asc
cat /tmp/arm-gnu-toolchain-12.3.rel1-aarch64-arm-none-eabi.tar.xz.sha256asc
```

This should generate the following output:
```
14c0487d5753f6071d24e568881f7c7e67f80dd83165dec5164b3731394af431  arm-gnu-toolchain-12.3.rel1-aarch64-arm-none-eabi.tar.xz
```

Compare that output with the output of:

```
sha256sum /tmp/arm-gnu-toolchain-12.3.rel1-aarch64-arm-none-eabi.tar.xz
```

The checkums should be the same:
```
14c0487d5753f6071d24e568881f7c7e67f80dd83165dec5164b3731394af431  /tmp/arm-gnu-toolchain-12.3.rel1-aarch64-arm-none-eabi.tar.xz
```

Now extract the toolchain and set the PICO_TOOLCHAIN_PATH environment variable to point to the toolchain:

```
mkdir -p ~/builds/
unxz /tmp/arm-gnu-toolchain-12.3.rel1-aarch64-arm-none-eabi.tar.xz
tar -x -f /tmp/arm-gnu-toolchain-12.3.rel1-aarch64-arm-none-eabi.tar -C ~/builds/
export PICO_TOOLCHAIN_PATH=~/builds/arm-gnu-toolchain-12.3.rel1-aarch64-arm-none-eabi
```

## MicroPython

If you don't already have them installed, install cmake and build-essential:

```
sudo apt install -y cmake build-essential
```

Get the MicroPython source code:

```
cd ~/builds/
git clone https://github.com/MicroPython/MicroPython
cd MicroPython
```

Build the MicroPython cross-compiler:

```
make -C mpy-cross
```

Get the Pico W MicroPython sub-modules:

```
make -C ports/rp2 submodules BOARD=RPI_PICO_W
```

Now make MicroPython for the Pico W:

```
make -C ports/rp2 -j 4 BOARD=RPI_PICO_W
```

You should now have a uf2 firmware image you can install on your Pico W:

```
ls -go ports/rp2/build-RPI_PICO_W/firmware.uf2
```

You should see something like this:
```
-rw-r--r-- 1 1607168 Sep  5 11:42 ports/rp2/build-RPI_PICO_W/firmware.uf2
```

## Installing and Running

Plug your Pico W into your Raspberry Pi while holding down the Pico's BOOTSEL button and figure out what device it is:


```
sudo dmesg |grep "Attached SCSI removable disk"
```

Will show for example:

```
[12307.427345] sd 0:0:0:0: [sda] Attached SCSI removable disk
```

This Pico W is /dev/sda.  We'll assume that below.  If you didn't see anything you probably failed to hold down BOOTSEL - try unplugging and replugging while holding down the button.

Mount /dev/sda1:

```
sudo mount /dev/sda1 /mnt
```

Copy the image you built onto the Pico and unmount the device:
```
sudo cp ~/builds/MicroPython/ports/rp2/build-RPI_PICO_W/firmware.uf2 /mnt/
sudo umount /mnt/
```

MicroPython should now be running on your Pi.  Use a serial terminal to connect to it via USB:
```
sudo apt install -y minicom
minicom -o -D /dev/ttyACM0
```

Hit enter and you should see a Python shell prompt:
```
>>>
```

Hit Ctrl-D to check it's the version you just built:
```
MPY: soft reboot
MicroPython v1.20.0-448-g5e5059373 on 2023-09-05; Raspberry Pi Pico W with RP2040
Type "help()" for more information.
>>>
```

Here:

* v1.20.0-448-g5e5059373 shows us the last git tag for the MicroPython repository we cloned (you can check this by running ```git describe``` within your MicroPython directory)
* 2023-09-05 shows us the date we built the firmware

You can exit minicom with Ctrl-A, then X, then Enter.

