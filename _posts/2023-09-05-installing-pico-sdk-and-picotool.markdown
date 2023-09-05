---
layout: post
title:  "Installing the Raspberry Pi Pico C SDK and picotool, on a Raspberry Pi"
date:   2023-09-05 7:02 +0000
tags:   raspberry pi pico sdk picotool bare metal
---

This post explains how to install the Pico C SDK and how to build and install picotool on a Raspberry Pi.

## Dependencies

Install the dependencies required by both the SDK and picotool:
```
sudo apt -y install build-essential pkg-config libusb-1.0-0-dev cmake
```

## Get the SDK

```
mkdir -p ~/builds
cd ~/builds
git clone https://github.com/raspberrypi/pico-sdk
cd pico-sdk
git submodule update --init
export PICO_SDK_PATH=~/builds/pico-sdk
```

## Get picotool

```
mkdir -p ~/builds
cd ~/builds
git clone https://github.com/raspberrypi/picotool
cd picotool
```

## Build picotool

```
export PICO_SDK_PATH=~/builds/pico-sdk
cd picotool
cmake .
make -j 4
```

## Install picotool

```
sudo make install
```

To be able to run picotools without needing sudo:

```
sudo cp udev/99-picotool.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules && sudo udevadm trigger
```

## Running picotool

```
picotool info -a
```

If you have a Pico in BOOTSEL mode, you should see something like - obviously depending on what you have installed, you may seen something different on your pi.

```
Program Information
 name:            MicroPython
 version:         v1.20.0-448-g5e5059373
 features:        thread support
                  USB REPL
 frozen modules:  aioble/security, aioble/l2cap, aioble/client, aioble/central, aioble/server,
                  aioble/peripheral, aioble/device, aioble/core, aioble, webrepl_setup, webrepl,
                  ntptime, mip, urequests, neopixel, dht, ds18x20, onewire, uasyncio, asyncio/stream,
                  asyncio/lock, asyncio/funcs, asyncio/event, asyncio/core, asyncio, _boot, _boot_fat,
                  rp2, main
 binary start:    0x10000000
 binary end:      0x100c431c
 embedded drive:  0x1012c000-0x10200000 (848K): MicroPython

Fixed Pin Information
 none

Build Information
 sdk version:       1.5.1
 pico_board:        pico_w
 boot2_name:        boot2_w25q080
 build date:        Sep  5 2023
 build attributes:  MinSizeRel

Device Information
 flash size:   2048K
 ROM version:  3
```

You can also use picotool to inspect a firmware file on your Pi:

```
picotool ~/builds/MicroPython/ports/rp2/build-RPI_PICO_W/firmware.uf2
```

Shows:

```
File /home/pi/builds/MicroPython/ports/rp2/build-RPI_PICO_W/firmware.uf2:

Program Information
 name:            MicroPython
 version:         v1.20.0-448-g5e5059373
 features:        thread support
                  USB REPL
 frozen modules:  aioble/security, aioble/l2cap, aioble/client, aioble/central, aioble/server,
                  aioble/peripheral, aioble/device, aioble/core, aioble, webrepl_setup, webrepl,
                  ntptime, mip, urequests, neopixel, dht, ds18x20, onewire, uasyncio, asyncio/stream,
                  asyncio/lock, asyncio/funcs, asyncio/event, asyncio/core, asyncio, _boot, _boot_fat,
                  rp2, main
 binary start:    0x10000000
 binary end:      0x100c431c
 embedded drive:  0x1012c000-0x10200000 (848K): MicroPython

Fixed Pin Information
 none

Build Information
 sdk version:       1.5.1
 pico_board:        pico_w
 boot2_name:        boot2_w25q080
 build date:        Sep  5 2023
 build attributes:  MinSizeRel
```